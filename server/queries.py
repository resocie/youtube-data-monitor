from server.api_exceptions import InvalidUsage
from server.models import db
from server.models import Actor, Videos
from datetime import datetime
from sqlalchemy import func
import json
import os


class DBYouTube:

    def get_dates():
        dates = db.session.query(Actor.collected_date).\
            order_by(Actor.collected_date.desc()).\
            distinct()
        all_dates = [item[0].strftime('%d-%m-%Y') for item in dates]

        return {'dates': all_dates}

    def get_info_actor(date, actor):
        actor = db.session.query(Actor).filter(Actor.collected_date == date,
                                               func.lower(Actor.actor_name) ==
                                               func.lower(actor)).first()
        if actor is not None:
            del actor.__dict__['_sa_instance_state']
            return actor.__dict__
        else:
            return None

    def get_actor_videos(date, channel_id):
        videos = db.session.query(Videos).\
            filter_by(collected_date=date,
                      channel_id=channel_id).all()

        all_videos = []
        if videos is not None:
            for item in videos:
                del item.__dict__['_sa_instance_state']
                all_videos.append(item.__dict__)

            return all_videos
        else:
            return None
