<h1 align=center>
    🤫 Last Whisper
</h1>

The ***LAST WHISPER*** has a key feature to transcribe the online video or audio resources as well as local files.

## 1. Setup
I highly recommend to use virtual environments through anaconda.
```shell
# venv
conda create --name last-whisper python=3.13
conda install ffmpeg

# requirements
pip install -r "requirements.txt"
```

## *Future Roadmap*

- A feature of separation of multiple speakers
- Supports of more options for execution

## *Acknowledgement*

This python program is an extended appliaction integrating [yt_dlp](https://github.com/yt-dlp/yt-dlp) and [whisper](https://github.com/openai/whisper).