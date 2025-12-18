import logging
from pathlib import Path
import shutil

from dynaconf import Dynaconf

SETTINGS_DIR = Path(__file__).parent.parent

default_settings = SETTINGS_DIR / "yt2podcast" / "default_settings.toml"
user_settings = SETTINGS_DIR / "settings.toml"



settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        str(default_settings),
        str(user_settings),
    ],
    merge_enabled = True
)

if not user_settings.exists() or not settings.youtube.api_key:
    shutil.copy(default_settings, user_settings)
    print("The first time you run yt2podcast you must configure at least YouTube API key on settings.toml\n\
It's free for this tool requirements: https://developers.google.com/youtube/v3/getting-started")
    exit(1)
