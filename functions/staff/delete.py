import json

from pynamodb.exceptions import DoesNotExist, DeleteError

from ..lib.response import response_no_data

from ..models.staff_model import StaffModel
from ..models.user_model import UserModel


def delete(event, context):
    try:
        staff_id = event['pathParameters']['staff_id']
    except:
        return response_no_data(status_code=400, message='Could not get staff_id')

    try:
        found_staff = StaffModel.get(hash_key=staff_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Staff not found')

    try:
        found_user = UserModel.get(hash_key=found_staff.user_id)

        found_staff.delete()
        found_user.delete()
    except DeleteError:
        return response_no_data(status_code=500, message='Could not delete staff')

    return response_no_data(status_code=200, message='Delete completed successfully')
