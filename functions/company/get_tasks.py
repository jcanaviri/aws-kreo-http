from ..lib.response import response_with_data, response_no_data

from ..models.task_model import TaskModel


def get_tasks_by_company_id(event, context):
    try:
        company_id = event['pathParameters']['company_id']
    except:
        return response_no_data(status_code=400, message='Could not get company_id')

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
    return response_with_data(status_code=200, data=body)
