import os

from datetime import datetime
from dotenv import load_dotenv

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute, NumberAttribute
from pynamodb.models import Model


class UserModel(Model):
    class Meta:
        table_name = 'usersTable'
        region = 'us-east-2'

        load_dotenv()
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY')

    user_id = UnicodeAttribute(hash_key=True, null=False)
    email = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)
    is_active = BooleanAttribute(null=False, default=True)
    is_password_change = BooleanAttribute(null=False, default=False)
    intent_counter = NumberAttribute(null=False, default=0)
    created_at = UTCDateTimeAttribute(null=False, default=datetime.now())
    updated_at = UTCDateTimeAttribute(null=False)

    # Override the save method to update the date
    def save(self, conditional_operator=None, **expected_values):
        self.updated_at = datetime.now()
        super(UserModel, self).save()
