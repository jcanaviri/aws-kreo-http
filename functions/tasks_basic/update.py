import json

from pynamodb.exceptions import DoesNotExist

from ..models.task_basic_model import TaskBasicModel

from ..lib.response import response_no_data, response_with_data


def update(event, context):
    try:
        task_basic_id = event['pathParameters']['task_basic_id']
    except:
        return response_no_data(status_code=400, message='Could not get task_basic_id')

    body = json.loads(event['body'])

    try:    
        title = body['title']
    except KeyError:
        title = event['title'] if 'title' in event else None
    
    try:
        description = body['description']
    except KeyError:
        description = event['description'] if 'description' in event else None

    try:
        found_task = TaskBasicModel.get(hash_key=task_basic_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Task Basic not found')
    except: 
        return response_no_data(status_code=500, message='Could not find task basic')

    if title:
        found_task.title = title
    if description:
        found_task.description = description
    found_task.save()

    body = {
        "task_basic_id": found_task.task_basic_id,
        "title": found_task.title,
        "description": found_task.description
    }
    return response_with_data(status_code=200, data=body)
