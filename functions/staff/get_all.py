import json

from ..lib.headers import headers

from ..models.staff_model import StaffModel
from ..models.company_model import CompanyModel
from ..models.user_model import UserModel


def get_all(event, context):
    staff_list = []

    for staff in StaffModel.scan():
        found_company = CompanyModel.get(hash_key=staff.company_id)
        found_user = UserModel.get(hash_key=staff.user_id)

        curr_staff = {
            "staff_id": staff.staff_id,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "email": found_user.email,
            "password": found_user.password,
            "is_active": found_user.is_active,
            "is_password_change": found_user.is_password_change,
            "address": staff.address,
            "phone": staff.phone,
            "document_number": staff.document_number,
            "document_type": staff.document_type,
            "boss": staff.boss,
            "job": staff.job,
            "image_url": staff.image_url,
            "created_at": str(found_user.created_at),
            "updated_at": str(found_user.updated_at),
            "company_id": staff.company_id,
            "company_name": found_company.name
        }
        staff_list.append(curr_staff)

    body = {
        "data": staff_list
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
