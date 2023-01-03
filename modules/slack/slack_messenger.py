from __future__ import annotations
from typing import Optional
from dataclasses import dataclass
from time import time
from slack_bolt import App
from slack_sdk.web import SlackResponse
from slack_sdk.models.attachments import Attachment
from .exceptions import ChannelNotDefined


@dataclass
class SlackMessenger:
    slack_token: str
    signing_secret: str
    channel: str = None

    def __post_init__(self):
        self.app = App(token=self.slack_token, signing_secret=self.signing_secret)

        self.client = self.app.client

    def set_channel(self, channel: str) -> SlackMessenger:
        self.channel = channel
        return self

    def process_response(self, response: SlackResponse) -> dict:
        return response.data

    def send_text_message(self, message: str, channel: str = None) -> Optional[dict]:
        if channel:
            self.set_channel(channel)

        if not self.channel:
            raise ChannelNotDefined()

        msg_response = self.client.chat_postMessage(channel=self.channel, text=message)

        return self.process_response(msg_response)

    def send_success_message(
        self, message: str, source: str, metadata: dict = None
    ) -> Optional[dict]:
        return self.send_attachment(message, source, "good", metadata)

    def send_error_message(
        self, message: str, source: str, metadata: dict = None
    ) -> Optional[dict]:
        return self.send_attachment(message, source, "danger", metadata)

    def send_attachment(
        self, message: str, source: str, color: str = "good", metadata: dict = {}
    ):

        color_map = {
            "good": ["pass", "success", "good", "ok"],
            "danger": [
                "fail",
                "danger",
                "error",
                "bad",
                "exception",
                "failed",
                "raise",
                "throw",
            ],
            "warning": ["warn", "warning", "info"],
        }

        for c, statuses in color_map.items():
            if color in statuses:
                color = c
                break

        att = (
            Attachment(
                fallback=message,
                color=color,
                text=message,
                fields=[
                    {"title": m.capitalize(), "value": metadata[m]}
                    for m in metadata.keys()
                ],
                pretext=f"A new message from {source}",
                footer=source,
                ts=time(),
            )
        ).to_dict()

        att["mrkdwn_in"] = ["fields"]

        msg_response = self.client.chat_postMessage(
            channel=self.channel,
            attachments=[att],
            # Strictly Attachment
            text="",
        )

        return self.process_response(msg_response)
