import json

from ..models.task_model import TaskModel

from ..lib.headers import headers


def get_all_basic_tasks(event, context):
    tasks_list = []

    for task in TaskModel.scan(TaskModel.task_type == 'basic'):
        curr_task = {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "task_type": task.task_type,
            "company_id": task.company_id
        }
        tasks_list.append(curr_task)

    body = {
        "data": tasks_list
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
