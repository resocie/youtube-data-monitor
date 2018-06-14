from server.models import Actor, db
from server.models import Videos
from server.main import app
from sqlalchemy import exc
import csv
import os

app.app_context().push()
db.create_all()  # create the tables and database

data_folders = [x[1] for x in os.walk('data/')][0]
for folder in data_folders:
    video_files = [x[2] for x in os.walk('data/'+folder+'/channel_videos')][0]
    for file in video_files:
        with open('data/'+folder+'/channel_videos/'+file, 'r') as video_file:
            video_reader = csv.DictReader(video_file)
            for row in video_reader:
                print(folder, file, row['title'])
                actor_info = db.session.query(Actor).filter_by(collected_date='04-06-2018', title=str(file).replace('.csv', '')).first()
                if actor_info.__dict__['channel_id'] != '' and actor_info.__dict__['channel_id'] != 'null':
                    try:
                        video_db = Videos(views=row['views'] if 'views' in row else None,
                                          title=row['title'] if 'title' in row else None,
                                          likes=row['likes'] if 'likes' in row else None,
                                          dislikes=row['dislikes'] if 'dislikes' in row else None,
                                          comments=row['comments'] if 'comments' in row else None,
                                          favorites=row['favorites'] if 'favorites' in row else None,
                                          publishedAt=row['publishedAt'] if 'publishedAt' in row else None,
                                          description=row['description'] if 'description' in row else None,
                                          url=row['url'] if 'url' in row else None,
                                          embeddable=row['embeddable'] if 'embeddable' in row else None,
                                          tags=row['tags'] if 'tags' in row else None,
                                          related_to_video=row['related_to_video'] if 'related_to_video' in row else None,
                                          category=row['category'] if 'category' in row else None,
                                          collected_date=folder,
                                          video_id=row['video_id'] if 'video_id' in row else None,
                                          thumbnail=row['thumbnail'] if 'thumbnail' in row else None,
                                          channel_id=actor_info.__dict__['channel_id'],
                                          duration=row['duration'] if 'duration' in row else None)

                        db.session.add(video_db)
                        db.session.commit()
                    except exc.IntegrityError:
                        db.session.rollback()
