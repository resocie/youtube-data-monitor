from youtube.youtube import YoutubeAPI
import csv
import json


def insert_actors_info():
    """ Check if actor has username.
        If so saves id and username on youtube.csv.
    Returns:
        YoutubeAPI object if successful, None otherwise.
    """
    yt_api = YoutubeAPI()
    yt_api.generate_folder()
    check = yt_api.generate_csv(clean=True)

    if check:
        with open('config/actors.json') as json_file:
            data = json.load(json_file)
            for item in data['channels']:
                if 'username' in item:
                        if item['username']:
                            result = yt_api.get_channel_info_by_username(
                                                            item['username'])
                            item['id'] = result['items'][0]['id']

                yt_api.insert_value(column='channel_id',
                                    value=item['id'],
                                    search_cell='actor',
                                    search_value=item['actor'].
                                    replace('\n', ''))

                yt_api.insert_value(column='username',
                                    value=item['username'],
                                    search_cell='actor',
                                    search_value=item['actor'].
                                    replace('\n', ''))
            return yt_api

    return None


def scrap_basic_actors_info():
    """ Scrap basic information about actors from grupos_politicos.csv.
        Puts it in a file called 'channels_basic_info.json'
        Basic info: Actor title, channel_id and username.
    """
    with open('data/grupos_politicos.csv', 'r') as csv_file:
        read_CSV = csv.DictReader(csv_file)
        actors_info = {}
        actors = []
        for row in read_CSV:
            sample_actors_info = {'actor': '', 'username': '', 'id': ''}

            if 'https' in row['YOUTUBE']:
                sample_actors_info['actor'] = row['FRENTES / COLETIVOS']

                if 'user' in row['YOUTUBE']:
                    url = row['YOUTUBE'].split('/')
                    index = url.index('user') + 1
                    sample_actors_info['username'] = url[index]
                    sample_actors_info['id'] = ''
                elif 'channel' in row['YOUTUBE']:
                    url = row['YOUTUBE'].split('/')
                    index = url.index('channel') + 1
                    sample_actors_info['id'] = url[index]
                    sample_actors_info['username'] = ''

                actors.append(sample_actors_info)

            elif 'S/' in row['YOUTUBE']:
                sample_actors_info['actor'] = row['FRENTES / COLETIVOS']
                sample_actors_info['id'] = ''
                sample_actors_info['username'] = ''
                actors.append(sample_actors_info)

    with open('data/channels_basic_info.json', 'w') as outfile:
        actors_info['channels'] = actors
        outfile.write(json.dumps(actors_info, sort_keys=True, indent=4))
