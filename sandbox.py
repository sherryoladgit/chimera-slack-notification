import json
import os
import boto3
from modules.run import process_message
from modules.logger import LoggerInstance
from modules.common import default_log_format

logger = LoggerInstance("SANDBOX", default_log_format()).logger
QUEUE_URL = os.getenv(
    "QUEUE_URL",
    "https://sqs.us-west-2.amazonaws.com/436445528296/chimera-slack-notification-dev-jobs",
)
SQS = boto3.client("sqs", region_name="us-west-2")


def producer(msg):
    status_code = 200
    message = ""

    try:
        SQS.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=msg,
        )
        message = "Message accepted!"
    except Exception as e:
        logger.exception("Sending message to SQS queue failed!")
        message = str(e)
        status_code = 500

    print({"statusCode": status_code, "body": json.dumps({"message": message})})


if __name__ == "__main__":

    message = """
Donec rutrum congue leo eget malesuada. Sed porttitor lectus nibh. Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Nulla porttitor accumsan tincidunt. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus.

Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Nulla porttitor accumsan tincidunt. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem. Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem.

Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Cras ultricies ligula sed magna dictum porta. Proin eget tortor risus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus.

        ```
        {
            code: 400,
            message: "It cannot be that bad
        }
        ```
        """

    record = {
        "body": json.dumps(
            {
                "type": "error",
                "body": message,
                "source": "sample-tool",
                "metadata": {
                    "pod": "pod-123456",
                    "namespace": "sample-tool",
                    "node": "i-0982732934",
                    "something": "else",
                },
                "channel": "C04FMSYQFF0",
            }
        )
    }

    # Process/test locally
    process_message(record)

    # Pricess with lambda function
    # Send to SQS queue
    producer(record["body"])
