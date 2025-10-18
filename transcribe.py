# built-in modules
import argparse
import os, io
from typing import List
from pathlib import Path

# constant
from constant.options import (
    DWL_OPT, CACHE_PATH,
    MODEL, TRANSCRIPTION_PATH
)

# utils
from utils.parser import (
    parse_arguments
)
from utils.utils import (
    join_path_str,
    remove_files
)

# core external modules
import yt_dlp
import whisper


def refine_download_option(args: argparse.Namespace):
    DWL_OPT['quiet'] = not args.verbose

def download_audio(urls: List[str]) -> List[str]:
    info = [] # download info
    file_path_info = [] # file_path info

    # download
    with yt_dlp.YoutubeDL(DWL_OPT) as ydl:
        for url in urls:
            info.append(ydl.extract_info(url, download=True))
    
    # append file path info
    for i in info:
        for v in (i.get("requested_downloads") or []):
            fp = v.get("filepath") or v.get("_filename")
        file_path_info.append(fp)
    
    return file_path_info # this info is used to transcribe and remove cache


def transcribe(tr: whisper.Whisper, sources: List[str]):
    for source in sources[1:]:
        result = tr.transcribe(source, 
                               verbose=args.verbose,
                               language=args.language
                               )
        save_transcription(result, source)
    return


def save_transcription(transcription: dict[str, str | list], f: str):
    # Refer to: json format -> transcriber_format.json 
    fp_txt = join_path_str(
        TRANSCRIPTION_PATH, 
        os.path.splitext( f.split('/')[-1] )[0] + '.txt'
    )
    buff = io.StringIO()   # buffer
    
    # save a file with timeline
    if args.timeline:
        lines = [
            f'[{seg['start']:.3} ---> {seg['end']:.3}] {seg['text']}\n' 
                for seg in transcription['segments']
        ]
    else:
        lines = [ f'{seg['text']}\n' for seg in transcription['segments'] ]
    buff.writelines(lines)
    
    # save file
    with open(fp_txt, 'w') as f:
        f.write(buff.getvalue()) # buffer write
    return


def main(args: argparse.Namespace):
    # main function    
    downloaded_files: List[str] = [CACHE_PATH]
    transcriber: whisper.Whisper = whisper.load_model(MODEL)

    # if the urls are given
    if args.url:
        # preprocessing
        save_dir = Path(CACHE_PATH)
        save_dir.mkdir(parents=True, exist_ok=True)

        print(f"Try getting audio source")
        refine_download_option(args)
        downloaded_files += download_audio(args.url)
        print(f"Complete downloading audio source")

    # local video file is extracted into audio file automatically in whisper

    # transcription
    print(f"Try transcribing the audio source(s)")
    transcribe(transcriber, downloaded_files)

    # postprocessing
    print(f"Try postprocessing")
    remove_files(downloaded_files)



if __name__ == "__main__":
    args = parse_arguments()
    main(args)
    
