from core.actors_info import scrap_basic_actors_info, insert_actors_info
from youtube.youtube import YoutubeAPI
from core.output import FileOutput
from youtube.videos import Videos
import json

# get data from grupos_politicos and insert data into youtube.csv
actors_info = scrap_basic_actors_info()
insert_actors_info(actors_info)

video = Videos()
youtube_user = YoutubeAPI()

with open('data/actors.json') as data_file:
    actors = json.load(data_file)
    actors = actors['actors']

    for actor in actors:
        # get ID from youtube.csv
        channel = youtube_user.get_row(column='actor', value=actor)
        channel_id = channel['channel_id']

        if channel_id:
            # get all info from channel
            response = youtube_user.get_channel_info(channel_id)
            title = youtube_user.get_channel_title(response)
            subscribers = youtube_user.get_channel_subscribers(response)
            video_count = youtube_user.get_channel_video_count(response)
            view_count = youtube_user.get_channel_total_view_count(response)

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

            videos_views = video.get_all_video_views_user_id(response, 5)

            if videos_views:
                output = FileOutput('channel_videos/' + title + '.csv')
                output.export_to_CSV(videos_views, ['title', 'views'])
