from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any
import urllib.error
import urllib.request


@dataclass
class TelegramSettings:
    bot_token: str
    chat_id: int
    allowed_username: str | None = None


class TelegramState:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = {"offset": 0}
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))

    def get_offset(self) -> int:
        return int(self.data.get("offset", 0))

    def set_offset(self, offset: int) -> None:
        self.data["offset"] = offset
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")


class TelegramClient:
    def __init__(self, settings: TelegramSettings) -> None:
        self.settings = settings
        self.base_url = f"https://api.telegram.org/bot{settings.bot_token}/"

    @classmethod
    def from_env(
        cls,
        *,
        bot_token_env: str,
        chat_id_env: str,
        allowed_username_env: str,
    ) -> "TelegramClient":
        bot_token = os.environ.get(bot_token_env, "").strip()
        chat_id = os.environ.get(chat_id_env, "").strip()
        if not bot_token or not chat_id:
            raise RuntimeError(
                f"Missing Telegram credentials. Expected env vars {bot_token_env} and {chat_id_env}."
            )
        allowed_username = os.environ.get(allowed_username_env, "").strip() or None
        return cls(
            TelegramSettings(
                bot_token=bot_token,
                chat_id=int(chat_id),
                allowed_username=allowed_username,
            )
        )

    def send_message(self, text: str) -> dict[str, Any]:
        return self._call(
            "sendMessage",
            {
                "chat_id": self.settings.chat_id,
                "text": text,
                "disable_web_page_preview": True,
            },
        )

    def get_updates(self, offset: int, timeout: int) -> list[dict[str, Any]]:
        return self._call(
            "getUpdates",
            {
                "offset": offset,
                "timeout": timeout,
                "allowed_updates": ["message"],
            },
        )

    def _call(self, method: str, payload: dict[str, Any]) -> Any:
        request = urllib.request.Request(
            self.base_url + method,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.load(response)
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Telegram API {method} failed: {details}") from exc

        if not data.get("ok"):
            raise RuntimeError(f"Telegram API {method} returned an error: {data}")
        return data["result"]
