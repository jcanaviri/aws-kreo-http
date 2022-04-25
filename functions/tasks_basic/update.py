import json

from pynamodb.exceptions import DoesNotExist

from ..models.task_basic_model import TaskBasicModel

from ..lib.response import response_no_data, response_with_data


def update(event, context):
    try:
        task_basic_id = event['pathParameters']['task_basic_id']
    except:
        return response_no_data(status_code=400, message='Could not get task_basic_id')

    try:
        body = json.loads(event['body'])
        
        title = body['title']
        description = body['description']
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        
    if title is None or description is None:
        return response_no_data(status_code=400, message='The body fields are invalid')

    try:
        found_task = TaskBasicModel.get(hash_key=task_basic_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Task Basic not found')
    except: 
        return response_no_data(status_code=500, message='Could not find task')

    found_task.title = title
    found_task.description = description
    found_task.save()

    body = {
        "task_basic_id": found_task.task_basic_id,
        "title": found_task.title,
        "description": found_task.description
    }
    return response_with_data(status_code=200, data=body)
