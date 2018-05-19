from core.actors_info import scrap_basic_actors_info, insert_actors_info
import youtube.youtube as yt
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

    for actor in actors:            # get ID from youtube.csv
        channel = youtube_user.get_row(column='actor', value=actor)
        channel_id = channel['channel_id']
        if channel_id:
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

            videos_views = video.get_all_video_views_user_id(response, 5)

            if videos_views:
                # saves videos on channel_videos folder
                directory = 'data/' + yt.start_time
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
                                                    'url'])
