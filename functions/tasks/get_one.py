import json

from pynamodb.exceptions import DoesNotExist

from ..lib.response import no_data
from ..lib.response import headers

from ..models.task_model import TaskModel

def get_one(event, context):
    try:
        task_id = event['pathParameters']['task_id']
    except:
        return no_data('COULD_NOT_GET_TASKS_ID')
    
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
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response
    except DoesNotExist:
        return no_data('TASK_NOT_FOUND')
    except:
        return no_data('COULD_NOT_FIND_TASK')
