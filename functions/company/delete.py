import json

from pynamodb.exceptions import DoesNotExist, DeleteError

from ..lib.headers import headers
from ..models.company_model import CompanyModel


def delete(event, context):
    try:
        company_id = event['pathParameters']['company_id']
    except:
        body = {
            "data": None,
            "message": "COULD_NOT_DELETE_COMPANY"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    try:
        found_company = CompanyModel.get(hash_key=company_id)
    except DoesNotExist:
        body = {
            "data": None,
            "message": "COMPANY_NOT_FOUND"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    try:
        found_company.delete()
    except DeleteError:
        body = {
            "data": None,
            "message": "UNABLE_TO_DELETE"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    body = {
        "data": None,
        "message": "COMPANY_DELETED"
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
