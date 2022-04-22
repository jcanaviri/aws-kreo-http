import json

from ..lib.headers import headers
from ..models.company_model import CompanyModel


def get_all(event, context):
    company_list = []
    for company in CompanyModel.scan():
        curr_company = {
            "company_id": company.company_id,
            "name": company.name,
            "nit": company.nit,
            "image": company.image
        }
        company_list.append(curr_company)

    body = {
        "data": company_list
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
