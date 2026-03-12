from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
import re
import sys
import time

from .models import ApprovalRequest, ApprovalResult, TelegramConfig
from .telegram import TelegramClient, TelegramState


class ApprovalProvider(ABC):
    @abstractmethod
    def request(self, approval_request: ApprovalRequest) -> ApprovalResult:
        raise NotImplementedError


class NullApprovalProvider(ApprovalProvider):
    def request(self, approval_request: ApprovalRequest) -> ApprovalResult:
        return ApprovalResult(
            approved=False,
            approver="n/a",
            channel="none",
            decided_at=datetime.now(timezone.utc),
            reason="Approval provider is disabled.",
        )


class ConsoleApprovalProvider(ApprovalProvider):
    def request(self, approval_request: ApprovalRequest) -> ApprovalResult:
        print("\n[Bastion approval required]", file=sys.stderr)
        print(approval_request.summary, file=sys.stderr)
        print(approval_request.details, file=sys.stderr)
        print("Type 'approve' to continue, anything else to reject:", file=sys.stderr)
        response = input("> ").strip().lower()
        approved = response == "approve"
        return ApprovalResult(
            approved=approved,
            approver="console",
            channel="console",
            decided_at=datetime.now(timezone.utc),
            reason="Manual console approval." if approved else "Console rejection.",
        )


class TelegramApprovalProvider(ApprovalProvider):
    def __init__(
        self,
        client: TelegramClient,
        state: TelegramState,
        *,
        timeout_seconds: int,
        poll_interval_seconds: int,
    ) -> None:
        self.client = client
        self.state = state
        self.timeout_seconds = timeout_seconds
        self.poll_interval_seconds = poll_interval_seconds

    @classmethod
    def from_config(
        cls,
        telegram: TelegramConfig,
        state_path,
        *,
        timeout_seconds: int,
        poll_interval_seconds: int,
    ) -> "TelegramApprovalProvider":
        client = TelegramClient.from_env(
            bot_token_env=telegram.bot_token_env,
            chat_id_env=telegram.chat_id_env,
            allowed_username_env=telegram.allowed_username_env,
        )
        return cls(
            client=client,
            state=TelegramState(state_path),
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )

    def request(self, approval_request: ApprovalRequest) -> ApprovalResult:
        message = (
            f"Approval needed\n"
            f"ID: {approval_request.request_id}\n\n"
            f"{approval_request.summary}\n\n"
            f"{approval_request.details}\n\n"
            f"Reply with:\n"
            f"approve {approval_request.request_id}\n"
            f"or\n"
            f"reject {approval_request.request_id}"
        )
        self.client.send_message(message)

        deadline = time.time() + approval_request.timeout_seconds
        approve_pattern = re.compile(rf"^(approve|reject)\s+{re.escape(approval_request.request_id)}$", re.I)

        while time.time() < deadline:
            updates = self.client.get_updates(self.state.get_offset(), self.poll_interval_seconds)
            for update in updates:
                self.state.set_offset(int(update["update_id"]) + 1)
                message = update.get("message") or {}
                if not self._is_authorized(message):
                    continue
                text = (message.get("text") or "").strip()
                match = approve_pattern.match(text)
                if not match:
                    continue
                approved = match.group(1).lower() == "approve"
                approver = message.get("from", {}).get("username") or str(message.get("from", {}).get("id"))
                return ApprovalResult(
                    approved=approved,
                    approver=approver,
                    channel="telegram",
                    decided_at=datetime.now(timezone.utc),
                    reason="Telegram approval." if approved else "Telegram rejection.",
                )

        return ApprovalResult(
            approved=False,
            approver="telegram-timeout",
            channel="telegram",
            decided_at=datetime.now(timezone.utc),
            reason="Approval timed out.",
        )

    def _is_authorized(self, message: dict[str, object]) -> bool:
        chat = message.get("chat", {})
        if int(chat.get("id", 0)) != self.client.settings.chat_id:
            return False
        if self.client.settings.allowed_username:
            username = (message.get("from", {}) or {}).get("username")
            if username != self.client.settings.allowed_username:
                return False
        return True
