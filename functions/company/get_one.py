import json

from ..lib.response import response_with_data, response_no_data

from ..models.company_model import CompanyModel


def get_one(event, context):
    # get the company_id
    try:
        company_id = event['pathParameters']['company_id']
    except:
        return response_no_data(status_code=400, message='Could not get company_id')

    for company in CompanyModel.query(hash_key=company_id):
        body = {
            "data": {
                "company_id": company.company_id,
                "name": company.name,
                "nit": company.nit,
                "image": company.image,
            },
        }

        return response_with_data(status_code=200, data=body)

    return response_no_data(status_code=404, message='Company not found')
