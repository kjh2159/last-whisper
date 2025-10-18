"""
DOWNLOAD OPTIONS
"""
CACHE_PATH = "./.cache/"
DWL_OPT = {
    "format": "bestaudio[ext=mp3]/m4a",    # download only audio stream
    "outtmpl": f"{CACHE_PATH}%(title)s.%(ext)s",
    # skip postprocessors (for optimization)
    "quiet": True, "no_warnings": True,
}



"""
TRANSCRIPTION OPTIONS
"""
MODEL = "turbo" # available: [tiny, base, small, medium, large, turbo]
TRANSCRIPTION_PATH = "./"