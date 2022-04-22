import json
import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

from ..lib.headers import headers


def send_phone_code(event, context):
    # Using twilio client
    load_dotenv()

    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )

    # Get the service_id created in twilio console
    service_id = os.getenv('TWILIO_SERVICE_ID')

    # This is because in AWS GetAway
    # event doesn't have a body
    try:
        body = json.loads(event['body'])

        country_code = body['country_code']
        phone_number = body['phone_number']
    except KeyError:
        country_code = event['country_code'] if 'country_code' in event else None
        phone_number = event['phone_number'] if 'phone_code' in event else None

    if country_code is None or phone_number is None \
        or type(country_code) != str or type(phone_number) != str:
        body = {
            "data": None,
            "message": "BAD_REQUEST"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    try:
        res = client \
            .verify.services(service_id) \
            .verifications.create(
                to=f'+{country_code}{phone_number}', 
                channel="sms"
            )

        body = {
            "data": {
                "sid": res.sid,
                "service_sid": res.service_sid,
                "account_sid": res.account_sid,
                "to": res.to,
                "channel": res.channel,
                "status": res.status,
                "valid": res.valid,
                "amount": res.amount,
                "payee": res.payee,
                "date_created": str(res.date_created),
                "date_updated": str(res.date_updated)
            }
        }

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

    except TwilioRestException:
        body = {
            "data": None,
            "message": "CAN'T_SEND_CODE"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response


def verify_phone_code(event, context):
    # Using twilio client
    load_dotenv()

    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )

    # Get the service_id created in twilio console
    service_id = os.getenv('TWILIO_SERVICE_ID')
    
    # This is because in AWS GetAway
    # event doesn't have a body
    try:
        body = json.loads(event['body'])
        country_code = body['country_code']
        phone = body['phone_number']
        code = body['code']
    except KeyError:
        country_code = event['country_code'] if 'country_code' in event else None
        phone = event['phone_number'] if 'phone_number' in event else None
        code = event['code'] if 'code' in event else None
    
    if country_code is None or phone_number is None or code is None\
        or type(country_code) != str or type(phone_number) != str or type(code) != str:
        body = {
            "data": None,
            "message": "BAD_REQUEST"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response
    
    
    if not isinstance(code, str):
        response = {
            "statusCode": 400,
            "headers": headers,
            "body": None,
            "message": "INVALID_CODE"
        }
        return response

    try:
        phone_number = f'+{country_code}{phone}'

        verification = client \
            .verify.services(service_id) \
            .verification_checks.create(
                to=phone_number, 
                code=code
            )
        body = {
            "data": {
                "sid": verification.sid,
                "service_sid": verification.service_sid,
                "account_sid": verification.account_sid,
                "to": verification.to,
                "channel": verification.channel,
                "status": verification.status,
                "valid": verification.valid,
                "date_created": str(verification.date_created),
                "date_updated": str(verification.date_updated),
                "amount": verification.amount,
                "payee": verification.payee
            }
        }

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response
    except TwilioRestException:
        body = {
            "data": None,
            "message": "CAN'T_VERIFY_CODE"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response
