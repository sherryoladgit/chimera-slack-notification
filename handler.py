from modules.run import process_message


def consumer(event, context):
    for record in event['Records']:
        process_message(record)
