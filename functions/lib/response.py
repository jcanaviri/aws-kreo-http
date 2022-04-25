import json

from .headers import headers


def response_no_data(status_code, message):
    body = {
        "data": None,
        "message": message
    }
    response = {"statusCode": status_code, "headers": headers, "body": json.dumps(body)}
    return response


def response_with_data(status_code, data):
    response = {"statusCode": status_code, "headers": headers, "body": json.dumps(data)}
    return response


def response_no_content(status_code):
    response = {"statusCode": status_code, "headers": headers}
    return response
    
