import json

from uuid import uuid1

from ..lib.headers import headers
from ..models.company_model import CompanyModel
from ..models.task_model import TaskModel
from ..models.task_basic_model import TaskBasicModel


def create(event, context):
    # form_data has two keys that handle the incoming data
    try:
        body = json.loads(event['body'])

        name = body["name"]
        nit = body["nit"]
        image = body["image"]
    except KeyError:
        name = event['name'] if 'name' in event else None
        nit = event['nit'] if 'nit' in event else None
        image = event['image'] if 'image' in event else None

    # if the values are None, or type is incorrect, or doest have content
    if name is None or nit is None or image is None or \
        type(name) != str or type(nit) != int or type(image) != str or \
        name == '' or image == '':
        body = {
            "data": None,
            "message": "BAD_REQUEST"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    new_company = CompanyModel(
        company_id=str(uuid1()),
        name=name,
        nit=nit,
        image=image
    )
    new_company.save()

    # When the company is created, create its basic tasks
    for basic_task in TaskBasicModel.scan():
        new_task = TaskModel(
            task_id=str(uuid1()),
            title=basic_task.title,
            description=basic_task.description,
            status=False,
            task_type='basic',
            company_id=new_company.company_id
        )
        new_task.save()


    body = {
        "company_id": new_company.company_id,
        "name": new_company.name,
        "nit": new_company.nit,
        "image": new_company.image
    }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(body)
    }
