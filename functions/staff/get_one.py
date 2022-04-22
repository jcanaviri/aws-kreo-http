import json

from pynamodb.exceptions import DoesNotExist, GetError

from ..lib.headers import headers
from ..lib.response import no_data

from ..models.staff_model import StaffModel
from ..models.company_model import CompanyModel
from ..models.user_model import UserModel


def get_one(event, context):
    # get the company_id
    try:
        staff_id = event['pathParameters']['staff_id']
    except:
        return no_data('COULD_NOT_GET_STAFF_ID')

    for staff in StaffModel.query(hash_key=staff_id):
        try:
            found_company = CompanyModel.get(hash_key=staff.company_id)
        except DoesNotExist:
            return no_data('STAFF_NOT_FOUND')
        except GetError:
            return no_data('COULD_NOT_GET_STAFF')

        try:
            found_user = UserModel.get(hash_key=staff.user_id)
        except DoesNotExist:
            return no_data('STAFF_NOT_FOUND')
        except GetError:
            return no_data('COULD_NOT_GET_STAFF')

        body = {
            "data": {
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
                "company_name": found_company.name,
                "company_id": staff.company_id,
                "user_id": staff.user_id,
            },
        }

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    return no_data('STAFF_NOT_FOUND')
