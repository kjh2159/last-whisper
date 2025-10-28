import os
from typing import Union, List
from pathlib import Path

import magic


def is_local_file(f: str) -> bool:
    if os.path.exists(f):
        return True
    return False


def get_file_type(filepath: str) -> str:
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(filepath)
    if file_type.startswith('audio/'):
        return 'audio'
    elif file_type.startswith('video/'):
        return 'video'
    return 'unknown'


def join_path_str(*parts: Union[str, Path]) -> str:
    """
    Join path parts and return a str.
    Example: join_path_str("a", "b") -> "a/b"
    Works with Path or str inputs.
    """
    return str(Path(*[str(p) for p in parts]))


def remove_files(paths: List[str]):
    paths.reverse() # due to CACHE_PATH
    unsafe = {Path('/').resolve(), Path.home().resolve()}
    for p in paths:
        try:
            path = Path(p)
            if not path.exists():
                continue # file not exist

            resolved = path.resolve()
            # safe guard
            if resolved in unsafe: # protect removing root or home directory
                print(f"Refusing to remove unsafe path: {resolved}")
                continue # Refuse and keep removing

            if resolved.is_dir():
                try:
                    resolved.rmdir() # empty directory
                except OSError:
                    pass # non-empty directory
                continue
            else:
                resolved.unlink() # unlink the file

        except Exception as e:
            print(f"Failed to remove '{p}': {e}")
            continue


# to check gpu usage
def print_model_device(tr):
    p = next(tr.parameters())
    print(f"[whisper] model.param.device={p.device}, dtype={p.dtype}")


def fmt_time(t_seconds: float, use_hours: bool) -> str:
    """sec -> formatting into HH:MM:SS or MM:SS"""
    t = int(t_seconds) 
    if use_hours:
        h = t // 3600
        m = (t % 3600) // 60
        s = t % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
    else:
        m = t // 60
        s = t % 60
        return f"{m:02d}:{s:02d}"

if __name__ == "__main__":
    print(get_file_type(".cache/test.webm"))