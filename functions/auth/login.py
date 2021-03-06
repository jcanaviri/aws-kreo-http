import json

from werkzeug.security import check_password_hash

from ..lib.auth_token import get_token
from ..lib.response import response_no_data, response_with_data

from ..models.user_model import UserModel
from ..models.staff_model import StaffModel
from ..models.company_model import CompanyModel


def login(event, context):
    # This is because in AWS GetAway
    # event doesn't have a body
    try:
        body = json.loads(event["body"])

        email = body.get('email')
        password = body.get('password')
    except KeyError:
        email = event['email'] if 'email' in event else None
        password = event['password'] if 'password' in event else None
    
    if email is None or password is None \
        or type(email) != str or type(password) != str:
        return response_no_data(status_code=400, message='Email or password cannot be blank')

    # Validate if the user exists
    for user in UserModel.scan(UserModel.email == email):
        if check_password_hash(user.password, password):
            if user.is_active:
                # set last_seen value
                user.intent_counter = 0
                user.save()

                # Session token
                auth_token = get_token(user.email)

                for staff in StaffModel.scan(StaffModel.user_id == user.user_id):
                    company = CompanyModel.get(hash_key=staff.company_id)

                    body = {
                        "data": {
                            "staff_id": staff.staff_id,
                            "first_name": staff.first_name,
                            "last_name": staff.last_name,
                            "email": user.email,
                            "password": user.password,
                            "is_active": user.is_active,
                            "is_password_change": user.is_password_change,
                            "auth_token": auth_token,
                            "address": staff.address,
                            "phone": staff.phone,
                            "document_number": staff.document_number,
                            "document_type": staff.document_type,
                            "boss": staff.boss,
                            "job": staff.job,
                            "image_url": staff.image_url,
                            "created_at": str(user.created_at),
                            "updated_at": str(user.updated_at),
                            "company_name": company.name,
                            "company_id": company.company_id,
                            "user_id": staff.user_id
                        }
                    }
                    return response_with_data(status_code=200, data=body)
            else:
                return response_no_data(status_code=403, message='User is blocked')
        else:
            # Incorrect password set counter += 1
            if user.intent_counter < 3:
                user.intent_counter += 1
                user.save()
                body = {
                    "data": None,
                    "intents": user.intent_counter,
                    "message": f"PASSWORD_INCORRECT_INTENT_{user.intent_counter}"
                }
                return response_with_data(status_code=401, data=body)

            # If the counter is greater than 3 block the user
            user.is_active = False
            user.save()
            return response_no_data(status_code=403, message='User is blocked')

    return response_no_data(status_code=404, message='User not found')
