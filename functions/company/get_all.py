from ..lib.response import response_with_data
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
    return response_with_data(status_code=200, data=body)
