from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
import logging
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from scraper import fetch_bouts, print_bouts

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
db_string = "postgresql://postgres@localhost:5432"
logger.debug(f'Connecting to database at {db_string}')
db = create_engine(db_string)
base = declarative_base()

def persist_fighter(session: Session, fighter_first: String, fighter_last) -> None:
    try:
        fighter = Fighter(fighter_first=fighter_first, fighter_last=fighter_last)
        session.add(fighter)
        session.commit()
        logger.info(f'Persisted {fighter_first + " " + fighter_last} to database.')
    except IntegrityError as e:
        logger.warning(f'Fighter already exists in database {fighter_first + " " + fighter_last}')
        session.rollback()

class Fighter(base):
    __tablename__ = 'fighters'
    fighter_id = Column(Integer, primary_key=True)
    fighter_first = Column(String)
    fighter_last = Column(String)

# class Weightclass(base):
#     __tablename__ = 'weightclasses'
#     weightclass_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     bouts = relationship('Bout')

# class Outcome(base):
#     __tablename__ = 'outcomes'
#     outcome_id = Column(Integer, primary_key=True)
#     name = Column(String)

class Bout(base):
    __tablename__ = 'bouts'
    bout_id = Column(Integer, primary_key=True)
    winner_id = Column(Integer, ForeignKey('fighters.fighter_id'))
    winner = relationship("Fighter", foreign_keys=[winner_id])
    loser_id = Column(Integer, ForeignKey('fighters.fighter_id'))
    loser = relationship("Fighter", foreign_keys=[loser_id])
    # weightclass_id = Column(Integer, ForeignKey('weightclasses.weightclass_id'))
    # weightclass = relationship("Weightclass", back_populates="weightclass")
    # outcome_id = Column(Integer, ForeignKey('outcomes.outcome_id'))
    # outcome = relationship('Outcome', back_populates="outcome")

session_setup = sessionmaker(db)
session = session_setup()
base.metadata.create_all(db)
bouts = fetch_bouts()
for bout in bouts:
    winner_first = bout['winner'].split(' ', 1)[0]
    winner_last = bout['winner'].split(' ', 1)[1]
    loser_first = bout['loser'].split(' ', 1)[0]
    loser_last = bout['loser'].split(' ', 1)[1]
    persist_fighter(session, winner_first, winner_last)
    persist_fighter(session, loser_first, loser_last)
