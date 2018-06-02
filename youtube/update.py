from core.actors_info import scrap_basic_actors_info, insert_actors_info
from youtube.youtube import YoutubeAPI
from core.output import FileOutput
from youtube.videos import Videos
from server.models import Actor, db
from server.models import Videos as VideosDB
from server.main import app
import time
import os
import json

# scrap_basic_actors_info()
youtube_user = insert_actors_info()
video = Videos()
app.app_context().push()
db.create_all()  # create the tables and database

with open('data/channels_basic_info.json') as data_file:
    actors = json.load(data_file)
    actors_dict = actors['channels']
    no_video_actors = []

    for actor in actors_dict:            # get ID from youtube.csv
        channel_id = actor['id']
        channel_username = actor['username']
        channel_actor = actor['actor']
        if channel_id != 'null' and channel_id:
            directory = 'data/' + YoutubeAPI.start_time
            # get all info from channel
            response = youtube_user.get_channel_info(channel_id)
            title = youtube_user.get_channel_title(response)
            subscribers = youtube_user.get_channel_subscribers(response)
            video_count = youtube_user.get_channel_video_count(response)
            view_count = youtube_user.get_channel_total_view_count(response)
            comment_count = youtube_user.get_channel_total_comment_count(
             response)
            creation_date = youtube_user.get_channel_creation_date(
             response)
            channel_thumbnail = youtube_user.get_channel_thumbnail(response)
            description = youtube_user.get_channel_description(response)
            keywords = youtube_user.get_channel_keywords(response)
            banner_thumbnail = youtube_user.get_channel_banner(response)
            hundred_thousand = youtube_user.check_above_one_hundred_thousand(
             subscribers)

            youtube_user.insert_value(column='subscribers',
                                      value=subscribers,
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='video_count',
                                      value=video_count,
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='view_count',
                                      value=view_count,
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='comment_count',
                                      value=comment_count,
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='creation_date',
                                      value=creation_date.split("T")[0],
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='thumbnail_url',
                                      value=channel_thumbnail,
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='description',
                                      value=description,
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='keywords',
                                      value=keywords,
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='banner_url',
                                      value=banner_thumbnail,
                                      search_cell='channel_id',
                                      search_value=channel_id)
            youtube_user.insert_value(column='above_one_hundred_thousand',
                                      value=str(hundred_thousand),
                                      search_cell='channel_id',
                                      search_value=channel_id)

            actor_db = Actor(actor_name=channel_actor,
                             actor_username=channel_username,
                             channel_id=channel_id,
                             title=title,
                             subscribers=subscribers,
                             video_count=video_count,
                             view_count=view_count,
                             comment_count=comment_count,
                             created_date=creation_date.split("T")[0],
                             collected_date=YoutubeAPI.start_time,
                             thumbnail_url=channel_thumbnail,
                             description=description,
                             keywords=keywords,
                             banner_url=banner_thumbnail,
                             above_one_hundred_thousand=hundred_thousand)

            db.session.add(actor_db)
            db.session.commit()
            print(actor_db)
            videos_views = video.get_all_video_views_user_id(response, 5)

            if videos_views:
                # saves videos on channel_videos folder
                channel_videos_folder = directory + '/channel_videos'
                if not os.path.exists(channel_videos_folder):
                    os.makedirs(channel_videos_folder)
                output = FileOutput(channel_videos_folder + '/' + title +
                                    '.csv')
                output.export_to_CSV(videos_views, ['id',
                                                    'title',
                                                    'views',
                                                    'likes',
                                                    'dislikes',
                                                    'comments',
                                                    'favorites',
                                                    'url',
                                                    'publishedAt',
                                                    'description',
                                                    'tags',
                                                    'embeddable',
                                                    'duration',
                                                    'thumbnail',
                                                    'related_to_video',
                                                    'video_category'
                                                    ])
                for item in videos_views:
                    video_db = VideosDB(views=item['views'],
                                        title=item['title'],
                                        likes=item['likes'],
                                        dislikes=item['dislikes'],
                                        comments=item['comments'],
                                        favorites=item['favorites'],
                                        url=item['url'],
                                        publishedAt=item['publishedAt'],
                                        description=item['description'],
                                        tags=item['tags'],
                                        embeddable=item['embeddable'],
                                        duration=item['duration'],
                                        thumbnail=item['thumbnail'],
                                        related_to_video=item
                                        ['related_to_video'],
                                        category=item['video_category'],
                                        collected_date=YoutubeAPI.start_time,
                                        channel_id=channel_id,
                                        video_id=item['id'])

                    db.session.add(video_db)
                    db.session.commit()
            else:
                no_video_actors.append({'actors': actor['actor']})
        else:
            headers = ['username', 'channel_id', 'subscribers', 'video_count',
                       'view_count', 'comment_count', 'creation_date',
                       'thumbnail_url', 'description', 'keywords',
                       'banner_url', 'above_one_hundred_thousand']
            youtube_user.insert_multiple_values(column=headers,
                                                search_cell='channel_id',
                                                search_value=channel_id)
    output = FileOutput(directory + '/no_video_actors.csv')
    output.export_to_CSV(no_video_actors)
