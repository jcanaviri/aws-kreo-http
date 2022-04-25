import json

from werkzeug.security import generate_password_hash
from pynamodb.exceptions import GetError, DoesNotExist

from ..lib.response import response_no_data, response_with_data

from ..models.user_model import UserModel
from ..models.staff_model import StaffModel
from ..models.company_model import CompanyModel


def change_password(event, context):
    # This is because in AWS event doesn't have a body
    try:
        body = json.loads(event['body'])
        # Get the post fields
        email = body.get('email')
        new_password = body.get('new_password')
    except KeyError:
        email = event['email'] if 'email' in event else None 
        new_password = event['new_password'] if 'new_password' in event else None

    # Validate if the request body is not in the right format
    if email is None or new_password is None \
        or type(email) != str or type(new_password) != str:
        return response_no_data(status_code=400, message="Email or password cannot be blank")

    for user in UserModel.scan(UserModel.email == email):
        # When the password is restored 
        # reset counter and status to true
        new_password = generate_password_hash(new_password)
        user.password = new_password
        user.intent_counter = 0
        user.is_active = True

        # This only executes the first time the user
        # enters on the site
        if not user.is_password_change:
            user.is_password_change = True

        user.save()

        # We get the staff and the company
        for found_staff in StaffModel.scan(StaffModel.user_id == user.user_id):
            try:
                found_company = CompanyModel.get(hash_key=found_staff.company_id)
            except GetError:
                return response_no_data(status_code=404, message="Company not found")
            except DoesNotExist:
                return response_no_data(status_code=404, message="Company not found")
                

            body = {
                "data": {
                    "staff_id": found_staff.staff_id,
                    "first_name": found_staff.first_name,
                    "last_name": found_staff.last_name,
                    "email": user.email,
                    "password": user.password,
                    "is_active": user.is_active,
                    "is_password_change": user.is_password_change,
                    "intent_counter": user.intent_counter,
                    "address": found_staff.address,
                    "phone": found_staff.phone,
                    "document_number": found_staff.document_number,
                    "document_type": found_staff.document_type,
                    "boss": found_staff.boss,
                    "job": found_staff.job,
                    "image_url": found_staff.image_url,
                    "create_at": str(user.created_at),
                    "updated_at": str(user.updated_at),

                    "company_name": found_company.name,
                    "company_id": found_company.company_id
                }
            }
            return response_with_data(status_code=200, data=body)

    return response_no_data(status_code=404, message='User not found')
