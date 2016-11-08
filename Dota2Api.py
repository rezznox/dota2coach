import dota2api
import threading
from sqlalchemy import create_engine
from Tables import Pick, Match, Base
from sqlalchemy.orm import sessionmaker
import time

engine = create_engine('mysql://armandota:suckmydick@localhost/dota2')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
INITIAL_SEQ_NUM = 2410784577

api = dota2api.Initialise("0BCA842811E391C022B682191F5BF624")

def get_next(the_matches):
    while True:
        time.sleep(10)
        last = store_matches_in_db(the_matches)
        the_matches = get_100_matches(last)

def get_100_matches(seq_number):
    try:
        return api.get_match_history_by_seq_num(start_at_match_seq_num=seq_number)
    except:
        return api.get_match_history_by_seq_num(start_at_match_seq_num=seq_number)

def store_matches_in_db(the_matches):
    last_match_seq = 0
    for match in list(the_matches['matches']):
        last_match_seq = match['match_seq_num']
        picks = []
        if match['lobby_type'] == 7:
            session.add(Match(match_id=match['match_id'], seq_number=match['match_seq_num'], duration=match['duration'], tower_status_radiant=match['tower_status_radiant'],
                              tower_status_dire=match['tower_status_dire'], barracks_status_radiant=match['barracks_status_radiant'], barracks_status_dire=match['barracks_status_dire']))
            leaver = False
            for pick in list(match['players']):
                if pick['leaver_status'] == 0:
                    pick_object = Pick(hero_id=pick['hero_id'], match=match['match_id'], kills=pick['kills'], deaths=pick['deaths'], assists=pick['assists'], gold=pick['gold'],
                                       last_hits=pick['last_hits'], denies=pick['denies'], gold_per_min=pick['gold_per_min'], xp_per_min=pick['xp_per_min'],
                                       gold_spent=pick['gold_spent'], hero_damage=pick['hero_damage'], tower_damage=pick['tower_damage'], hero_healing=pick['hero_healing'],
                                       level=pick['level'])
                    picks.append(pick_object)
                else:
                    leaver = True
                    break
            #Transaction
            if not leaver:
                try:
                    session.commit()
                    for picked in picks:
                        session.add(picked)
                    session.commit()
                except:
                    session.rollback()
                    print('repetido: ' + str(last_match_seq))
            else:
                session.rollback()
                continue
    print('finished adding')
    return last_match_seq

matches = get_100_matches(INITIAL_SEQ_NUM)

get_next(matches)
