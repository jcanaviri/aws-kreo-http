import os

from dotenv import load_dotenv

from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute
from pynamodb.models import Model


class HolidayModel(Model):
    class Meta:
        table_name = 'holidaysTable'
        region = 'us-east-2'

        load_dotenv()
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY')

    holiday_id = UnicodeAttribute(hash_key=True, null=False)
    year = NumberAttribute(null=False)
    country = UnicodeAttribute(null=False)
    company = UnicodeAttribute(null=False)
    event_list = ListAttribute()
