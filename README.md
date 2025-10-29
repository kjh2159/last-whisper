<h1 align=center>
    🤫 Last Whisper
</h1>

The ***LAST WHISPER*** has a key feature to transcribe the online video or audio resources as well as local files.

## 0. Demo
<video controls muted playsinline width="720" src="https://github.com/user-attachments/assets/56b500f6-b06a-4fff-a612-c7498b4b0583"></video>

## 1. Setup

I highly recommend to use virtual environments through anaconda.
```shell
# clone repository
git clone https://github.com/kjh2159/last-whisper.git
cd last-whisper

# venv
conda create --name last-whisper python=3.13
conda activate last-whisper
conda install ffmpeg

# requirements
pip install -r "requirements.txt"
```

**🍎MacOS** should run the following command also. However, GPU operations are not supported on MacOS.

```shell
brew install libmagic
```

## 2. Usage

To use ***LAST WHISPER***, please refer to the following examples or options, the next section. 
> **⚠️**
> To use it, you should make private huggingface token. 
> <br>Please refer to huggingface site [here](https://huggingface.co/) for signing up and creating huggingface token.

### *A. Basic usage*
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

### *B. Diarization mode*
```shell
# basic diarization mode 
python transcribe.py --url "https://youtube.com/video1" --sd # or --speaker-diarization
```

```shell
# diarization with timeline
python transcribe.py --url "https://youtube.com/video1" --sd --timeline
```


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

## *Issues*

Please let me know about issues you are going through to `issue` or `discussion` tab!

## *Future Roadmap*

- [X] A feature of separation of multiple speakers
- [ ] Supports of more options for execution (task, output_format, temperature, etc.)

## *Acknowledgement*

This python program is an extended appliaction integrating [yt_dlp](https://github.com/yt-dlp/yt-dlp), [whisper](https://github.com/openai/whisper), and [whisperX](https://github.com/m-bain/whisperX).