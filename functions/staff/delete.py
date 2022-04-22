import json

from pynamodb.exceptions import DoesNotExist, DeleteError

from ..lib.headers import headers
from ..lib.response import no_data

from ..models.staff_model import StaffModel
from ..models.user_model import UserModel


def delete(event, context):
    try:
        staff_id = event['pathParameters']['staff_id']
    except:
        return no_data('COULD_NOT_GET_STAFF_ID')

    try:
        found_staff = StaffModel.get(hash_key=staff_id)
    except DoesNotExist:
        return no_data('STAFF_NOT_FOUND')

    try:
        found_user = UserModel.get(hash_key=found_staff.user_id)

        found_staff.delete()
        found_user.delete()
    except DeleteError:
        return no_data('COULD_NOT_DELETE')

    body = {
        "data": None,
        "message": "STAFF_DELETED"
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response
