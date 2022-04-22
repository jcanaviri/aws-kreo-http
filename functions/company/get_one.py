import json

from ..lib.headers import headers
from ..lib.response import no_data

from ..models.company_model import CompanyModel


def get_one(event, context):
    # get the company_id
    try:
        company_id = event['pathParameters']['company_id']
    except:
        body = {
            "data": None,
            "message": "COULD_NOT_GET_COMPANY"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    for company in CompanyModel.query(hash_key=company_id):
        body = {
            "data": {
                "company_id": company.company_id,
                "name": company.name,
                "nit": company.nit,
                "image": company.image,
            },
        }

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    return no_data('COMPANY_NOT_FOUND')
