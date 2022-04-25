import json

from uuid import uuid1
from pynamodb.exceptions import DoesNotExist

from ..lib.response import response_no_data, response_with_data
from ..models.holiday_model import HolidayModel


def register_holidays(event, context):
    """POST create new holiday"""
    try:
        body = json.loads(event['body'])

        year = body['year']
        country = body['country']
        company = body['company']
        event_list = body['event_list']
    except KeyError:
        year = event['year'] if 'year' in event else None
        country = event['country'] if 'country' in event else None
        company = event['company'] if 'company' in event else None
        event_list = event['event_list'] if 'event_list' in event else None

    if year is None or country is None or company is None or event_list is None \
        or type(year) != int or type(country) != str or \
            type(company) != str or type(event_list) != list:
        return response_no_data(status_code=400, message='The fields are invalid')

    new_holiday = HolidayModel(
        holiday_id = str(uuid1()),
        year=year,
        country=country,
        company=company,
        event_list=event_list
    )
    new_holiday.save()

    body = {
        "data": {
            "holiday_id": new_holiday.holiday_id,
            "year": new_holiday.year,
            "country": new_holiday.country,
            "company": new_holiday.company,
            "event_list": new_holiday.event_list
        },
    }
    return response_with_data(status_code=201, data=body)


def get_holidays(event, context):
    """GET all holidays by year"""
    try:
        year = event['queryStringParameters']['year']
    except:
        return response_no_data(status_code=400, message="You must provide a year")

    holidays_list = []
    for holiday in HolidayModel.scan(HolidayModel.year == int(year)):
        curr_holiday = {
            "holiday_id": holiday.holiday_id,
            "year": holiday.year,
            "country": holiday.country,
            "company": holiday.company,
            "event_list": holiday.event_list
        }
        holidays_list.append(curr_holiday)

    body = {
        "data": holidays_list
    }
    return response_with_data(status_code=200, data=body)


def update_holiday(event, context):
    """PUT update one holiday"""
    # get the holiday_id
    try: 
        holiday_id = event['pathParameters']['holiday_id']
    except:
        return response_no_data(status_code=400, message='Could not get holiday_id')
        
    # get the body
    try:
        body = json.loads(event['body'])

        year = body['year']
        country = body['country']
        company = body['company']
        event_list = body['event_list']
    except KeyError:
        year = event['year'] if 'year' in event else None
        country = event['country'] if 'country' in event else None
        company = event['company'] if 'country' in event else None
        event_list = event['event_list'] if 'event_list' in event else None

    if holiday_id is None or year is None or country is None or company is None or event_list is None \
        or type(year) != int or type(country) != str or \
            type(company) != str or type(event_list) != list:
        return response_no_data(status_code=400, message='The fields are not valid')

    try:
        found_holiday = HolidayModel.get(hash_key=holiday_id)
    except DoesNotExist:
        return response_no_data(status_code=404, data='Holiday not found')

    # Update the holiday
    found_holiday.year = year
    found_holiday.country = country
    found_holiday.company = company
    found_holiday.event_list = event_list

    found_holiday.save()

    body = {
        "data": {
            "holiday_id": found_holiday.holiday_id,
            "year": found_holiday.year,
            "country": found_holiday.country,
            "company": found_holiday.company,
            "event_list": found_holiday.event_list
        },
    }

    return response_with_data(status_code=200, data=body)
