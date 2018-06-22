from server.models import Actor, Videos, Relationship_Videos
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

    def is_not_video_in_db(video_id, date, channel_id):
        format_date = datetime.strptime(date, '%d-%m-%Y').date()
        video = db.session.query(Videos).filter(Videos.collected_date ==
                                                format_date,
                                                Videos.channel_id ==
                                                channel_id,
                                                Videos.video_id ==
                                                video_id).first()
        return video is None

    def add_relationship_videos(child_video_id,
                                parent_date, parent_channel_id, parent_url):
        relationship = Relationship_Videos(
                                            video_id=child_video_id,
                                            collected_date=parent_date,
                                            channel_id=parent_channel_id,
                                            original_video_url=parent_url
        )

        db.session.add(relationship)
        db.session.commit()
