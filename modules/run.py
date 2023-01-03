import os
import json
from .common import (
    get_aws_secret,
    basic_log_format,
    default_log_format,
    catch_basic_exception,
)
from .logger import LoggerInstance
from .slack.slack_messenger import SlackMessenger

IN_LAMBDA = os.environ.get("AWS_EXECUTION_ENV") is not None

logger = LoggerInstance(
    "CHIMERA_SLACK_NOTIFICATION",
    basic_log_format() if IN_LAMBDA else default_log_format(),
).logger

SLACK_CREDENTIALS_PARAMETER = "chimera/slackbot/credentials"
AWS_REGION = "us-west-2"
DEFAULT_SLACK_CHANNEL = "C04FMSYQFF0"


@catch_basic_exception(logger)
def process_message(message):

    message = json.loads(message["body"])

    logger.info(f"Processing Message: {message}")

    channel = message.get("channel", DEFAULT_SLACK_CHANNEL)
    message_type = message.get("type", "success")
    body = message.get("body", None)

    if not body:
        logger.error(f"Message has no body to send")
        exit(1)

    source = message.get("source", "Chimera")
    meta = message.get("metadata", {})

    slack_credentials = get_aws_secret(SLACK_CREDENTIALS_PARAMETER, AWS_REGION)

    logger.info("Fetching slack credentials from secret manager")
    if not slack_credentials:
        logger.error(
            (
                "Slack credentials not stored in secret manager,"
                f"expects `{SLACK_CREDENTIALS_PARAMETER}` to be available in `{AWS_REGION}`"
            )
        )
        exit(1)

    slack_credentials = json.loads(slack_credentials)
    slack = SlackMessenger(
        slack_credentials["token"], slack_credentials["signing_secret"], channel
    )

    # Usage with dynamic method
    # method = getattr(slack, f"send_{message_type}_message", None)
    # if not callable(method):
    #     logger.error(f"Unknown message type {message_type}")
    #     exit(1)
    # send = method(body, source, meta)

    logger.info("Sending slack message")
    send = slack.send_attachment(
        message=body, source=source, color=message_type, metadata=meta
    )
    logger.info(send)
