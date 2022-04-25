import json

from pynamodb.exceptions import DoesNotExist

from ..models.company_model import CompanyModel
from ..models.task_model import TaskModel

from ..lib.response import response_no_data, response_with_data


def update(event, context):
    try:
        task_id = event['pathParameters']['task_id']
    except:
        return response_no_data(status_code=400, message='Could not get task_id')
        
    try:
        body = json.loads(event['body'])

        title = body['title']
        description = body['description']
        status = body['status']
        company_id = body['company_id']
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        status = event['status'] if 'status' in event else None
        company_id = event['company_id'] if 'company_id' in event else None
        
    if title is None or description is None or status is None or company_id is None:
        return response_no_data(status_code=400, message='The body fiels are invalid')

    try:
        found_company = CompanyModel.get(hash_key=company_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Company not found')
    except: 
        return response_no_data(status_code=500, message='Could not find company')
    
    try:
        found_task = TaskModel.get(hash_key=task_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Task not found')
    except: 
        return response_no_data(status_code=500, message='Could not find task')

    found_task.title = title
    found_task.description = description
    found_task.status = status
    found_task.company_id = found_company.company_id
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

    return response_with_data(status_code=200, data=body)
