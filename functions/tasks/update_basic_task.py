import json

from pynamodb.exceptions import DoesNotExist

from ..models.task_model import TaskModel

from ..lib.response import no_data
from ..lib.headers import headers


def update_basic_task(event, context):
    try:
        task_id = event['pathParameters']['task_id']
    except:
        return no_data('COULD_NOT_GET_TASKS_ID')

    try:
        body = json.loads(event['body'])
        
        title = body['title']
        description = body['description']
        status = body['status']
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        status = event['status'] if 'status' in event else None
        
    if title is None or description is None or status is None:
        return no_data('BAD_REQUEST')

    try:
        found_task = TaskModel.get(hash_key=task_id)
    except DoesNotExist:
        return no_data('TASK_NOT_FOUND')
    except: 
        return no_data('COULD_NOT_FIND_TASK')

    if found_task.task_type != 'basic':
        return no_data('TASK_IS_NOT_BASIC')

    found_task.title = title
    found_task.description = description
    found_task.status = status
    found_task.save()

    body = {
        "data": {
            "task_id": found_task.task_id,
            "title": found_task.title,
            "description": found_task.description,
            "status": found_task.status,
            "task_type": found_task.task_type,
            "company_id": found_task.company_id
        }
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
