from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Match(Base):
    __tablename__ = 'match'
    match_id = Column(BigInteger, primary_key=True)
    seq_number = Column(BigInteger, unique=True, nullable=False)
    duration = Column(Integer, nullable=False)
    tower_status_radiant = Column(Integer, nullable=False)
    tower_status_dire = Column(Integer, nullable=False)
    barracks_status_radiant = Column(Integer, nullable=False)
    barracks_status_dire = Column(Integer, nullable=False)

class Pick(Base):
    __tablename__ = 'pick'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hero_id = Column(Integer, nullable=False)
    match = Column(BigInteger, ForeignKey('match.match_id'), nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    gold = Column(Integer, nullable=False)
    last_hits = Column(Integer, nullable=False)
    denies = Column(Integer, nullable=False)
    gold_per_min = Column(Integer, nullable=False)
    xp_per_min = Column(Integer, nullable=False)
    gold_spent = Column(Integer, nullable=False)
    hero_damage = Column(Integer, nullable=False)
    tower_damage = Column(Integer, nullable=False)
    hero_healing = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)

engine = create_engine('mysql://armandota:suckmydick@localhost/dota2')
Base.metadata.create_all(engine)