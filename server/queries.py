from server.models import Actor, Videos
from datetime import datetime
from sqlalchemy import func
from server import db
import json


class DBYouTube:

    def get_all_actors_name():
        with open('config/actors.json') as data_file:
            actors_json = json.load(data_file)
            actors_name = [name['actor'] for name in actors_json['channels']]
        return actors_name

    def get_dates():
        dates = db.session.query(Actor.collected_date).\
            order_by(Actor.collected_date.desc()).\
            distinct()
        all_dates = [item[0].strftime('%d-%m-%Y') for item in dates]

        return {'dates': all_dates}

    def get_info_actor(date, actor):
        format_date = datetime.strptime(date, '%d-%m-%Y').date()
        actor = db.session.query(Actor).filter(Actor.collected_date ==
                                               format_date,
                                               func.lower(Actor.actor_name) ==
                                               func.lower(actor)).first()
        if actor is not None:
            del actor.__dict__['_sa_instance_state']
            return actor.__dict__
        else:
            return None

    def get_actor_videos(date, channel_id):
        format_date = datetime.strptime(date, '%d-%m-%Y').date()
        videos = db.session.query(Videos).\
            filter_by(collected_date=format_date,
                      channel_id=channel_id).all()

        all_videos = []
        if videos is not None:
            for item in videos:
                del item.__dict__['_sa_instance_state']
                all_videos.append(item.__dict__)

            return all_videos
        else:
            return None
