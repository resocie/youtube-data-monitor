from youtube.youtube import YoutubeAPI
from core.get_info_actors import get_actors_info
import json

#get data from grupos_politicos and insert data into youtube.csv
yt = get_actors_info()
yt.read_actors_info()


youtubeUser = YoutubeAPI()

with open('data/actors.json') as data_file:
    actors = json.load(data_file)
    actors = actors['atores']
    for actor in actors:
        #get ID from youtube.csv
        channel = youtubeUser.get_data(param='ator', data=actor)
        id = channel['channel_id']

        if(id):
            #get all info from channel
            response = youtubeUser.get_channel_info(id)
            subscribers = youtubeUser.get_channel_subscribers(response)
            videoCount = youtubeUser.get_channel_video_count(response)
            viewCount = youtubeUser.get_channel_total_view_count(response)

            youtubeUser.insert_data(param='subscribers',
                                        value=subscribers,
                                        field_name='channel_id',
                                        field_value=id)
            youtubeUser.insert_data(param='video_count',
                                        value=videoCount,
                                        field_name='channel_id',
                                        field_value=id)
            youtubeUser.insert_data(param='view_count',
                                        value=viewCount,
                                        field_name='channel_id',
                                        field_value=id)
