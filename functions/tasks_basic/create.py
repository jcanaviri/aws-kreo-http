import json

from uuid import uuid1

from ..models.task_basic_model import TaskBasicModel
from ..lib.response import no_data
from ..lib.headers import headers


def create(event, context):
    try:
        body = json.loads(event['body'])

        title = body['title']
        description = body['description']
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        
    if title is None or description is None:
        return no_data('BAD_REQUEST')

    new_task = TaskBasicModel(
        task_basic_id=str(uuid1()),
        title=title,
        description=description
    )

    new_task.save()

    body = {
        "task_basic_id": new_task.task_basic_id,
        "title": new_task.title,
        "description": new_task.description,
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
