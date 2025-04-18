import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField
from wtforms.validators import DataRequired

from app.models.banner_record import BannerRecord
from app.models.mix_record import MixRecord


class MixCreateForm(FlaskForm):
    class Meta:
        # TODO: re-enable CSRF protection
        csrf = False

    title = StringField("Title", validators=[DataRequired()])
    system = StringField("System", validators=[DataRequired()])
    region = StringField("Region", validators=[DataRequired()])
    release = DateField("Release", validators=[DataRequired()], format="%Y-%m-%d")
    banner = FileField("Banner")

    def to_entity(self) -> MixRecord:
        banner = None
        if self.banner.data:
            banner = BannerRecord(blob=self.banner.data.read())

        return MixRecord(
            id=uuid.uuid4(),
            title=self.title.data,
            system=self.system.data,
            region=self.region.data,
            release=self.release.data,
            banner=banner,
        )
