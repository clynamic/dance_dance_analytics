from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models.simfile_record import SimfileRecord
from app.models.song_record import SongRecord


def load_simfile(simfile_text: str) -> SimfileRecord:
    simfile_record = SimfileRecord.from_string(simfile_text)
    sim = simfile_record.simfile

    song = SongRecord.from_sim(sim)
    song.simfile = simfile_record

    simfile_record.song = song

    return simfile_record
