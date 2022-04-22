import os

from dotenv import load_dotenv

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class StaffModel(Model):
    class Meta:
        table_name = 'staffTable'
        region = 'us-east-2'

        load_dotenv()
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY')

    staff_id = UnicodeAttribute(hash_key=True, null=False)
    first_name = UnicodeAttribute(null=False)
    last_name = UnicodeAttribute(null=False)
    address = UnicodeAttribute(null=False)
    phone = UnicodeAttribute(null=False)
    document_number = UnicodeAttribute(null=False)
    document_type = UnicodeAttribute(null=False)
    boss = UnicodeAttribute(null=False)
    job = UnicodeAttribute(null=False)
    image_url = UnicodeAttribute(null=False)
    company_id = UnicodeAttribute(null=False)
    user_id = UnicodeAttribute(null=False)
