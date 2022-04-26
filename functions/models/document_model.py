import os

from dotenv import load_dotenv

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class DocumentModel(Model):
    class Meta:
        table_name = 'documentsTable'
        region = 'us-east-2'

        load_dotenv()
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY')

    document_id = UnicodeAttribute(hash_key=True, null=False)
    title = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=False)
    company_id = UnicodeAttribute(null=False)
