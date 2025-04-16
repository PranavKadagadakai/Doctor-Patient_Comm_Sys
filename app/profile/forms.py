from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional

class ProfileForm(FlaskForm):
    full_name = StringField("Full Name", validators=[Optional()])
    role = StringField("Role", validators=[Optional()])
    age = IntegerField("Age", validators=[Optional()])
    phone = StringField("Phone", validators=[Optional()])
    address = StringField("Address", validators=[Optional()])
    submit = SubmitField("Save")
