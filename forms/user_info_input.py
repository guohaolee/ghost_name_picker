from wtforms import Form, StringField, validators
from wtforms.validators import DataRequired

class UserInfoInput(Form):
    """ user info form """

    first_name = StringField('first_ame', [
        validators.DataRequired(message=('Don\'t be shy!'))
    ])

    last_name = StringField('last_name', [
        validators.DataRequired(message=('Don\'t be shy!'))
    ])