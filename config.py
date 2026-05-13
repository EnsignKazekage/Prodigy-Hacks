"""
Local config loader - stores token and child IDs in user home directory.
Tokens are never transmitted anywhere except to Prodigy's own API.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict


CONFIG_DIR  = Path.home() / ".prodigy-companion"
CONFIG_FILE = CONFIG_DIR / "config.json"


def _ensure_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    _ensure_dir()
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(config: Dict):
    _ensure_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    try:
        os.chmod(CONFIG_FILE, 0o600)
    except Exception:
        pass


def get_token() -> Optional[str]:
    return load_config().get("token")


def get_default_user() -> Optional[str]:
    return load_config().get("defaultUser")


def set_token(token: str):
    cfg = load_config()
    cfg["token"] = token
    save_config(cfg)


def set_default_user(user_id: str):
    cfg = load_config()
    cfg["defaultUser"] = user_id
    save_config(cfg)


def get_screen_time_limit() -> int:
    return int(load_config().get("screenTimeLimitMinutes", 60))


def set_screen_time_limit(minutes: int):
    cfg = load_config()
    cfg["screenTimeLimitMinutes"] = minutes
    save_config(cfg)
