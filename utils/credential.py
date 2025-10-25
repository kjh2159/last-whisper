from __future__ import annotations
import os
from pathlib import Path
from getpass import getpass

from dotenv import load_dotenv, find_dotenv, set_key

def ensure_env_and_load(env_file: str = ".env") -> Path:
    """Ensure that the .env file exists and load environment variables from it."""
    found = find_dotenv(usecwd=True)
    dotenv_path = Path(found) if found else Path(env_file)
    
    if not dotenv_path.exists():
        dotenv_path.touch(exist_ok=True)
        try:
            # only POSIX systems
            os.chmod(dotenv_path, 0o600)
        except Exception:
            pass  # ignore if not POSIX
    load_dotenv(dotenv_path=dotenv_path, override=False)
    return dotenv_path

def require_credential(
        key: str, prompt_text: str = None, confirm: bool = True,
        min_length: int = 1, default: str = None) -> str:
    """Ensure that the specified credential is set in the environment variables."""
    value = os.getenv(key)
    if value and len(value) >= min_length:
        return value
    
    # prompt input by user
    # prompt_text is for softer message
    prompt = "If you don't have one, please create it first at https://huggingface.co/settings/tokens!\n"
    prompt += prompt_text or f"\tEnter your {key}: "
    while True:
        entered = getpass(f"{prompt}: ") or (default or "")
        if confirm:
            entered2 = getpass(f"\tConfirm your {key}: ")
            if entered != entered2:
                print("Token values do not match. Please try again.")
                continue
        if len(entered) < min_length:
            print(f"Token value must be at least {min_length} characters long. Please try again.")
            continue
        value = entered
        break

    # save to .env file
    dotenv_path = ensure_env_and_load()
    set_key(str(dotenv_path), key, value)

    # load to memory
    os.environ[key] = value
    
    # masking inform
    masked = value[:6] + "*"*6 if len(value) >= 6 else "***"
    print(f"Credential for '{key}' is set to: {masked}")

    return value