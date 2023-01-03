from os import getenv
import logging
import time
from typing import Callable
import boto3
import logging
import base64
from botocore.exceptions import ClientError


def catch_basic_exception(logger: logging.Logger = None, message: str = None) -> Callable:
    """
    Catch all the exceptions, log them and not break the application

    Args:
        func (Callable): The wrapped function
        message (str, optional): The friendly message to show
        logger (logging.Logger, optional): An instance of a logger to use

    Returns:
        Callable: A wrapped function with generic caught exception
    """
    from functools import wraps

    def inner(func: Callable):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                msg = message if message else repr(e)
                if logger:
                    logger.error(msg)
                    logging.error(repr(e))
                else:
                    logging.error(msg)
                    logging.error(repr(e))
                if bool(getenv('DEBUG', False)):
                    raise
        return wrapped
    return inner


def remove_metadata(func: Callable) -> Callable:

    def inner(*args, **kwargs):
        do = func(*args, **kwargs)
        if do and "ResponseMetadata" in do:
            del do['ResponseMetadata']
        return do
    return inner


def sts_client():
    return boto3.client('sts', region_name="us-west-2")


@remove_metadata
def whoami():
    return sts_client().get_caller_identity()


def basic_log_format():
    return logging.Formatter('%(message)s\n')


def default_log_format():
    return logging.Formatter("%(asctime)s : %(name)s : %(levelname)s : %(message)s")


def get_aws_secret(secret_name, region_name='us-west-2'):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        return base64.b64decode(get_secret_value_response['SecretBinary'])
