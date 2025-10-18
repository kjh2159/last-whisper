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
conda activate last-whisper

# clone repository
git clone https://github.com/kjh2159/last-whisper.git
cd last-whisper

# requirements
pip install -r "requirements.txt"
```

## 2. Usage

To use ***LAST WHISPER***, please refer to the following examples or options, the next section. 

```shell
# basic usage (url)
python transcribe.py --url "https://youtube.com/video1"
```

```shell
# basic usage (local file)
python transcribe.py --url "audio.mp3"
```

```shell
# language setting
python transcribe.py --url "https://youtube.com/video1" --language ko
```
> **TIP**: The program would detect video language if you do not specify the language.

```shell
# multiple urls or files
python transcribe.py --url "https://youtube.com/video1" "https://youtube.com/video2"
```

```shell
# see also verbose progress
python transcribe.py --url "https://youtube.com/video1" --verbose
```

```shell
# save result with timeline
python transcribe.py --url "https://youtube.com/video1" --timeline
```

> **TIP**: Other online video sources (e.g., vimeo) are available except for YouTube.

## 3. Options

To see available options, run the following command.
```shell
python transcribe.py --help
```

## 4. Customization

To customize the execution, see `constant/options.py`.<br>
From this, you can change the pre-set model, `turbo`.
```py
# constant/options.py
MODEL='small'
```
> **TIP**: Highly recommend use turbo model.

## *Future Roadmap*

- A feature of separation of multiple speakers
- Supports of more options for execution

## *Acknowledgement*

This python program is an extended appliaction integrating [yt_dlp](https://github.com/yt-dlp/yt-dlp) and [whisper](https://github.com/openai/whisper).