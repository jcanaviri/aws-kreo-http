import os

from dotenv import load_dotenv

from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model


class CompanyModel(Model):
    class Meta:
        table_name = 'companiesTable'
        region = 'us-east-2'

        load_dotenv()
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY')

    company_id = UnicodeAttribute(hash_key=True, null=False)
    name = UnicodeAttribute(null=False)
    nit = NumberAttribute(null=False)
    image = UnicodeAttribute(null=False)
