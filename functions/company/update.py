import json

from ..lib.headers import headers
from ..models.company_model import CompanyModel


def update(event, context):
    # get the company_id
    try:
        company_id = event['pathParameters']['company_id']
    except:
        body = {
            "data": None,
            "message": "COULD_NOT_UPDATE_COMPANY"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    try:
        body = json.loads(event["body"])

        name = body.get('name')
        nit = body.get('nit')
        image = body.get('image')
    except KeyError:
        name = event['name'] if 'name' in event else None
        nit = event['nit'] if 'nit' in event else None
        image = event['image'] if 'image' in event else None

    if name is None or nit is None or image is None or \
        type(name) != str or type(nit) != int or type(image) != str or \
        name == '' or image == '':
        body = {
            "data": None,
            "message": "BAD_REQUEST"
        }
        response = { "statusCode": 200, "headers": headers, "body": json.dumps(body)}

    for company in CompanyModel.query(hash_key=company_id):
        company.name = name
        company.nit = nit
        company.image_url = image
        company.save()

        body = {
            "data": {
                "company_id": company.company_id,
                "name": company.name,
                "nit": company.nit,
                "image_url": company.image_url
            },
        }

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    body = {
        "data": None,
        "message": "COMPANY_NOT_FOUND"
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
