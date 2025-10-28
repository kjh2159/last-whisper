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
from utils.credential import (
    ensure_env_and_load,
    require_credential
)

# core external modules
import yt_dlp
import whisper
import whisperx
import gc
from whisperx.diarize import DiarizationPipeline


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
    results = []
    audios = []
    for source in sources[1:]:
        audio = whisper.load_audio(source)  # pre-load to avoid cuda out of memory
        result = tr.transcribe(audio, 
                               verbose=args.verbose,
                               language=args.language
                               )
        audios.append(audio)
        results.append(result)
        if args.speaker_diarization:
            save_transcription(result, source)
    return audios, results


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


def diarize(audios: List[str], results: List[dict], sources: List[str], hf_token: str, device: str):
    for i, source in enumerate(sources[1:]):
        # for test
        # model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        # alignment = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        # print(alignment["segments"])

        diarize_model = DiarizationPipeline(use_auth_token=hf_token, device=device)
        diarize_segments = diarize_model(audios[i])
        result = whisperx.assign_word_speakers(diarize_segments, results[i])

        print(diarize_segments)
        for seg in result["segments"]:
            print(f"{seg["speaker"]}: {seg["text"]}")

def main(args: argparse.Namespace):
    # dotenv_path = ensure_env_and_load() # ensure .env file (make if not exists)
    if args.speaker_diarization:
        ensure_env_and_load()
        hf_token = require_credential(
            key="HUGGINGFACE_TOKEN", confirm=False
        )

    # main function    
    device = "cuda"
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
    audios, results = transcribe(transcriber, downloaded_files)
    print(f"Complete transcribing the audio source(s)")

    if args.speaker_diarization:
        print(f"Try speaker diarization")
        diarize(audios, results, downloaded_files, hf_token, device)
        print(f"Complete speaker diarization")

    # postprocessing
    print(f"Try postprocessing")
    remove_files(downloaded_files)



if __name__ == "__main__":
    args = parse_arguments()
    main(args)
    
