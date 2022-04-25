import json

from ..lib.response import response_no_data, response_with_data
from ..models.company_model import CompanyModel


def update(event, context):
    # get the company_id
    try:
        company_id = event['pathParameters']['company_id']
    except:
        return response_no_data(status_code=400, message='Could not get company_id')

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
        return response_no_data(status_code=400, message='The fields are invalid')

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

        return response_with_data(status_code=200, data=body)

    return response_no_data(status_code=404, message='Company not found')
