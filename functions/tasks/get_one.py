import json

from pynamodb.exceptions import DoesNotExist

from ..lib.response import response_no_data, response_with_data

from ..models.task_model import TaskModel


def get_one(event, context):
    try:
        task_id = event['pathParameters']['task_id']
    except:
        return response_no_data(status_code=400, message='Could not get task_id')
    
    try:
        found_tasks = TaskModel.get(hash_key=task_id)
        body = {
            "task_id": found_tasks.task_id,
            "title": found_tasks.title,
            "description": found_tasks.description,
            "status": found_tasks.status,
            "task_type": found_tasks.task_type,
            "company_id": found_tasks.company_id
        }
        return response_with_data(status_code=200, data=body)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Task not found')
    except:
        return response_no_data(status_code=500, message='Could not delete task')
        
