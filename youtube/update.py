from youtube.youtube import YoutubeAPI
from core.get_info_actors import get_actors_info
from core.output import FileOutput
from youtube.videos import Videos
import json

#get data from grupos_politicos and insert data into youtube.csv
yt = get_actors_info()
yt.read_actors_info()
video = Videos()
youtubeUser = YoutubeAPI()


with open('data/actors.json') as data_file:
    actors = json.load(data_file)
    actors = actors['atores']
    i = 1
    for actor in actors:
        #get ID from youtube.csv
        channel = youtubeUser.get_data(param='ator', data=actor)
        id = channel['channel_id']
        if(id):
            #get all info from channel
            response = youtubeUser.get_channel_info(id)
            title = youtubeUser.get_channel_title(response)
            print(str(i)+' - '+title)
            i=i+1
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

            videosViews = video.get_all_Video_Views_user_ID(response,5)
            if(videosViews!=[]):
                file = FileOutput('channel_videos/' + title + '.csv')
                file.export_CSV(videosViews,['Título','Número de visualizações'])
