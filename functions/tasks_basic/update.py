import json

from pynamodb.exceptions import DoesNotExist

from ..models.task_basic_model import TaskBasicModel

from ..lib.response import no_data
from ..lib.headers import headers


def update(event, context):
    try:
        task_basic_id = event['pathParameters']['task_basic_id']
    except:
        return no_data('COULD_NOT_GET_BASIC_TASKS_ID')

    try:
        body = json.loads(event['body'])
        
        title = body['title']
        description = body['description']
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        
    if title is None or description is None:
        return no_data('BAD_REQUEST')

    try:
        found_task = TaskBasicModel.get(hash_key=task_basic_id)
    except DoesNotExist:
        return no_data('TASK_NOT_FOUND')
    except: 
        return no_data('COULD_NOT_FIND_TASK')

    found_task.title = title
    found_task.description = description
    found_task.save()

    body = {
        "data": {
            "task_basic_id": found_task.task_basic_id,
            "title": found_task.title,
            "description": found_task.description
        }
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
