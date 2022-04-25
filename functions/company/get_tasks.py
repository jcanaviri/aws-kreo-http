import json

from ..lib.response import no_data
from ..lib.headers import headers
from ..models.task_model import TaskModel


def get_tasks_by_company_id(event, context):
    try:
        company_id = event['pathParameters']['company_id']
    except:
        return no_data('COULD_NOT_GET_COMPANY')

    # Get the basic tasks
    task_list = []
    for task in TaskModel.scan(TaskModel.company_id == company_id):
        curr_task = {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "task_type": task.task_type,
            "company_id": task.company_id
        }
        task_list.append(curr_task)
    body = {
        "data": task_list
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
