import json

from .headers import headers


def no_data(message):
    body = {
        "data": None,
        "message": message
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
