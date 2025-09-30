# Copyright (c) 2025 AshokShau
# Licensed under the GNU AGPL v3.0: https://www.gnu.org/licenses/agpl-3.0.html
# Part of the TgMusicBot project. All rights reserved where applicable.

import os
import shutil
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from TgMusic.logger import LOGGER

load_dotenv()


class BotConfig:
    """
    A class to manage and validate all bot configuration settings from environment variables.
    """

    def __init__(self):
        # Core Bot Configuration
        self.API_ID: Optional[int] = self._get_env_int("API_ID")
        self.API_HASH: Optional[str] = os.getenv("API_HASH")
        self.TOKEN: Optional[str] = os.getenv("TOKEN")

        self.SESSION_STRINGS: list[str] = self._get_session_strings()
        self.MONGO_URI: Optional[str] = os.getenv("MONGO_URI")
        self.DB_NAME: str = os.getenv("DB_NAME", "MusicHub Test")
        self.API_URL: str = os.getenv("API_URL", "https://tgmusic.fallenapi.fun")
        self.API_KEY: Optional[str] = os.getenv("API_KEY")

        # Owner and Logger
        self.OWNER_ID: int = self._get_env_int("OWNER_ID", 0)
        self.LOGGER_ID: int = self._get_env_int("LOGGER_ID", 0)

        # Health check server port
        self.RENDER_PORT: int = self._get_env_int("RENDER_PORT", default=10000)

        # Optional Settings
        self.PROXY: Optional[str] = os.getenv("PROXY")
        self.DEFAULT_SERVICE: str = os.getenv("DEFAULT_SERVICE", "youtube").lower()
        self.MIN_MEMBER_COUNT: int = self._get_env_int("MIN_MEMBER_COUNT", 50)
        self.MAX_FILE_SIZE: int = self._get_env_int("MAX_FILE_SIZE", 500 * 1024 * 1024)  # 500MB

        self.DOWNLOADS_DIR: Path = Path(os.getenv("DOWNLOADS_DIR", "database/music"))

        self.SUPPORT_GROUP: str = os.getenv(
            "SUPPORT_GROUP", "https://t.me/Free_Vpn_Chats"
        )
        self.SUPPORT_CHANNEL: str = os.getenv(
            "SUPPORT_CHANNEL", "https://t.me/Megahubbots"
        )

        self.START_IMG: str = os.getenv(
            "START_IMG",
            "https://i.pinimg.com/1200x/e8/89/d3/e889d394e0afddfb0eb1df0ab663df95.jpg",
        )

        self.IGNORE_BACKGROUND_UPDATES: bool = self._get_env_bool(
            "IGNORE_BACKGROUND_UPDATES", True
        )
        self.AUTO_LEAVE: bool = self._get_env_bool("AUTO_LEAVE", False)

        # Cookies
        self.COOKIES_URL: list[str] = self._process_cookie_urls(
            os.getenv("COOKIES_URL")
        )

        # Developer
        devs_env: Optional[str] = os.getenv("DEVS")
        self.DEVS: list[int] = list(map(int, devs_env.split())) if devs_env else []
        if self.OWNER_ID and self.OWNER_ID not in self.DEVS:
            self.DEVS.append(self.OWNER_ID)

        # Validate configuration
        self._validate_config()

    @staticmethod
    def _get_env_int(name: str, default: Optional[int] = None) -> Optional[int]:
        value = os.getenv(name)
        try:
            return int(value)
        except (TypeError, ValueError):
            LOGGER.warning(
                "Invalid value for %s: %s (default: %s)", name, value, default
            )
            return default

    @staticmethod
    def _get_env_bool(name: str, default: bool = False) -> bool:
        return os.getenv(name, str(default)).lower() == "true"

    @staticmethod
    def _get_session_strings(prefix: str = "STRING", count: int = 10) -> list[str]:
        return [
            s.strip() for i in range(1, count + 1) if (s := os.getenv(f"{prefix}{i}"))
        ]

    @staticmethod
    def _process_cookie_urls(value: Optional[str]) -> list[str]:
        if not value:
            return []
        return [url.strip() for url in value.replace(",", " ").split() if url.strip()]

    def _validate_config(self) -> None:
        missing = [
            name
            for name in ("API_ID", "API_HASH", "TOKEN", "MONGO_URI", "LOGGER_ID", "DB_NAME", "START_IMG")
            if not getattr(self, name)
        ]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")

        if not isinstance(self.MONGO_URI, str):
            raise ValueError("MONGO_URI must be a string")

        if not self.SESSION_STRINGS:
            raise ValueError("At least one session string (STRING1–10) is required")

        if self.IGNORE_BACKGROUND_UPDATES:
            db_path = Path("database")
            if db_path.exists():
                shutil.rmtree(db_path)

        try:
            self.DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
            Path("database/photos").mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create required directories: {e}") from e


config: BotConfig = BotConfig()
