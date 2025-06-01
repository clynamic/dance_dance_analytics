import uuid
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileSize
from wtforms import StringField, DateField, FileField
from wtforms.validators import DataRequired

from app.models.banner_record import BannerRecord
from app.models.mix_record import MixRecord


class MixCreateForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    system = StringField("System", validators=[DataRequired()])
    region = StringField("Region", validators=[DataRequired()])
    release = DateField("Release", validators=[DataRequired()], format="%Y-%m-%d")
    banner = FileField(
        "Banner",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Banner must be an image"),
            FileSize(max_size=5 * 1024 * 1024),
        ],
    )

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
