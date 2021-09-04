from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship

db_string = "postgresql://postgres@localhost:5432"
db = create_engine(db_string)
base = declarative_base()

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
fighter = Fighter(fighter_first="Alistair", fighter_last="Overeem")
session.add(fighter)
session.commit()
fighter = Fighter(fighter_first="Matt", fighter_last="Brown")
session.add(fighter)
session.commit()
fighters = session.query(Fighter)
for combatant in fighters:
    print(f'{combatant.fighter_first} {combatant.fighter_last}')