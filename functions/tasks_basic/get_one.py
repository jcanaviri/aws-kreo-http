import json

from pynamodb.exceptions import DoesNotExist

from ..models.task_basic_model import TaskBasicModel

from ..lib.response import response_no_data, response_with_data


def get_one(event, context):
    try:
        task_basic_id = event['pathParameters']['task_basic_id']
    except:
        return response_no_data(status_code=400, message='Could not get tasks_basic_id')

    try:
        found_task = TaskBasicModel.get(hash_key=task_basic_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Task Basic not found')
    except: 
        return response_no_data(status_code=500, message='Could not get task')

    body = {
        "task_basic_id": found_task.task_basic_id,
        "title": found_task.title,
        "description": found_task.description
    }
    return response_with_data(status_code=200, data=body)
