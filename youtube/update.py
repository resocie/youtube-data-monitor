from core.actors_info import scrap_basic_actors_info, insert_actors_info
from youtube.youtube import YoutubeAPI
from core.output import FileOutput
from youtube.videos import Videos
import time
import os
import json

# scrap_basic_actors_info()
youtube_user = insert_actors_info()
video = Videos()

with open('data/actors.json') as data_file:
    actors = json.load(data_file)
    actors = actors['actors']
    no_video_actors = []

    for actor in actors:            # get ID from youtube.csv
        channel = youtube_user.get_row(column='actor', value=actor)
        channel_id = channel['channel_id']
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

            videos_views = video.get_all_video_views_user_id(response, 5)

            if videos_views:
                channel_videos_related = directory + '/channel_videos_related'
                if not os.path.exists(channel_videos_related):
                    os.makedirs(channel_videos_related)
                for video_item in videos_views:
                    if 'related_to_video' in video_item:
                        related_videos = video_item['related_to_video']
                        del video_item['related_to_video']
                    else:
                        related_videos = 'disabled'
                    if related_videos != 'disabled':
                        output = FileOutput(channel_videos_related +
                                            '/' +
                                            video_item['title'].replace('/',
                                                                        ' ') +
                                            '.csv')
                        output.export_to_CSV(related_videos, ['original_title',
                                                              'original_id',
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
                                                              'video_category'
                                                              ])
                # saves videos on channel_videos folder
                channel_videos_folder = directory + '/channel_videos'
                if not os.path.exists(channel_videos_folder):
                    os.makedirs(channel_videos_folder)
                output = FileOutput(channel_videos_folder + '/' + title +
                                    '.csv')
                output.export_to_CSV(videos_views, ['title',
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
                                                    'video_category'
                                                    ])
            else:
                no_video_actors.append({'actors': actor})
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
