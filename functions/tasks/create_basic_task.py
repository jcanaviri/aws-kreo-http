import json

from uuid import uuid1

from ..models.task_model import TaskModel
from ..lib.response import no_data
from ..lib.headers import headers


def create_basic_task(event, context):
    try:
        body = json.loads(event['body'])

        title = body['title']
        description = body['description']
        status = body['status']
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        status = event['status'] if 'status' in event else None
        
    if title is None or description is None:
        return no_data('BAD_REQUEST')
    if not status:
        status = False

    new_task = TaskModel(
        task_id=str(uuid1()),
        title=title,
        description=description,
        status=status,
        task_type='basic'
    )

    new_task.save()

    body = {
        "task_id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "task_type": new_task.task_type
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
