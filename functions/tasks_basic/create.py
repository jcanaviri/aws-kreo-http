import json

from uuid import uuid1

from ..models.task_basic_model import TaskBasicModel
from ..lib.response import response_no_data, response_with_data


def create(event, context):
    try:
        body = json.loads(event['body'])

        title = body['title']
        description = body['description']
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        
    if title is None or description is None:
        return response_no_data(status_code=400, message='The body fields are invalid')

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
    return response_with_data(status_code=201, data=body)
