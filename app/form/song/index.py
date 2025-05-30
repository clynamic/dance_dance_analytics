from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional


class SongIndexForm(FlaskForm):
    title = StringField("Title", validators=[Optional()])
    artist = StringField("Artist", validators=[Optional()])
    mix_title = StringField("Mix Title", validators=[Optional()])
