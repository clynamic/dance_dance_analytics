from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional


class MixIndexForm(FlaskForm):
    title = StringField("Title", validators=[Optional()])
    system = StringField("System", validators=[Optional()])
    region = StringField("Region", validators=[Optional()])
