from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField
from wtforms.validators import DataRequired
from app.models.mix_record import MixRecord
from app.models.song_record import SongRecord
from app.models.banner_record import BannerRecord
from app.parser.load import load_simfile


class SongCreateForm(FlaskForm):
    mix_slug = StringField("Mix Slug", validators=[DataRequired()])
    simfile = FileField(
        "Simfile",
        validators=[
            FileAllowed(["sm", "ssc"], "Simfile must be .sm or .ssc"),
            FileSize(max_size=5 * 1024 * 1024),
            DataRequired(),
        ],
    )
    banner = FileField(
        "Banner",
        validators=[
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Banner must be an image"),
            FileSize(max_size=5 * 1024 * 1024),
        ],
    )

    def to_entity(self) -> SongRecord:
        mix = MixRecord.by_slug(self.mix_slug.data)
        if not mix:
            raise ValueError("Mix not found")

        simfile_data = self.simfile.data.read()
        simfile_text = simfile_data.decode("utf-8")

        record = load_simfile(simfile_text)
        record.song.mix_id = mix.id

        if self.banner.data:
            record.song.banner = BannerRecord(blob=self.banner.data.read())

        return record.song
