import json


def api(event, context):
    body = {
        "message": "Welcome to Grupo Kreo api"
    }

    response = {"statusCode": 200, "body": json.dumps(body), "input": event}

    return response
