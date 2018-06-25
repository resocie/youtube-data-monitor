from server.models import Actor, db
from server.models import Videos
from server.main import app
import csv
import os

def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False

app.app_context().push()
db.create_all()  # create the tables and database


data_folders = [x[1] for x in os.walk('data/')][0]

for folder in data_folders:
    with open('data/'+folder+'/youtube.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['channel_id'] != '' and row['channel_id'] != 'null':
                actor_db = Actor(actor_name=row['actor'] if 'actor' in row and row['actor'] != 'null' and row['actor'] != '' else '',
                                 actor_username=row['username'] if 'username' in row and row['username'] != 'null' and row['username'] != '' else '',
                                 channel_id=row['channel_id'] if 'channel_id' in row and row['channel_id'] != 'null' and row['channel_id'] != '' else '',
                                 subscribers=row['subscribers'] if 'subscribers' in row and row['subscribers'] != 'null' and row['subscribers'] != '' else None,
                                 title=row['title'] if 'title' in row and row['title'] != 'null' and row['title'] != '' else '',
                                 view_count=row['view_count'] if 'view_count' in row and row['view_count'] != 'null' and row['view_count'] != '' else None,
                                 comment_count=row['comment_count'] if 'comment_count' in row and row['comment_count'] != 'null' and row['comment_count'] != '' else None,
                                 created_date=row['creation_date'] if 'creation_date' in row and row['creation_date'] != 'null' and row['creation_date'] != '' else '',
                                 collected_date=row['collected_date'] if 'collected_date' in row and row['collected_date'] != 'null' and row['collected_date'] != '' else folder,
                                 thumbnail_url=row['thumbnail_url'] if 'thumbnail_url' in row and row['thumbnail_url'] != 'null' and row['thumbnail_url'] != '' else '',
                                 description=row['description'] if 'description' in row and row['description'] != 'null' and row['description'] != '' else '',
                                 keywords=row['keywords'] if 'keywords' in row and row['keywords'] != 'null' and row['keywords'] != ''else '',
                                 banner_url=row['banner_url'] if 'banner_url' in row and row['banner_url'] != 'null' and row['banner_url'] != '' else '',
                                 video_count=row['video_count'] if 'video_count' in row and row['video_count'] != 'null' and row['video_count'] != '' else None,
                                 above_one_hundred_thousand=str_to_bool(row['above_one_hundred_thousand']) if 'above_one_hundred_thousand' in row and row['above_one_hundred_thousand'] != '' else None)

                db.session.commit()
                db.session.add(actor_db)
