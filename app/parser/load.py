from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models.simfile_record import SimfileRecord
from app.models.song_record import SongRecord


def load_simfile(simfile_text: str) -> SimfileRecord:
    try:
        simfile_record = SimfileRecord.from_string(simfile_text)

        with db.session.begin():
            db.session.add(simfile_record)

            sim = simfile_record.simfile

            song = SongRecord.from_sim(sim)
            song.simfile = simfile_record
            db.session.add(song)

        return simfile_record

    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Simfile import failed (possible duplicate): {e}")
