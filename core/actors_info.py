from youtube.youtube import YoutubeAPI
import csv


def insert_actors_info(actors_info):
    """ Check if actor has username.

    If so saves id and username on youtube.csv.

    Args:
        actors_info (``list`` of ``dict``): Basic actors information.
    Returns:
        bool: True if successful, False otherwise.
    """
    yt_api = YoutubeAPI()
    check = yt_api.generate_csv(clean=True)

    if check:
        for item in actors_info:
            if item['username']:
                result = yt_api.get_channel_info_by_username(item['username'])
                item['id'] = result['items'][0]['id']
            yt_api.insert_value(column='channel_id',
                                value=item['id'],
                                search_cell='actor',
                                search_value=item['actor'].replace('\n', ''))
            yt_api.insert_value(column='username',
                                value=item['username'],
                                search_cell='actor',
                                search_value=item['actor'].replace('\n', ''))
        return True

    return False


# @TODO scrap and put in a json instead of scrap everytime
def scrap_basic_actors_info():
    """ Scrap basic information about actors from grupos_politicos.csv.

    Actor title, channel_id and username.

    Returns:
        ``list`` of ``dict``: Basic actors information.
    """
    with open('data/grupos_politicos.csv', 'r') as csv_file:
        read_CSV = csv.DictReader(csv_file)
        actors_info = []

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

                actors_info.append(sample_actors_info)
            elif 'S/' in row['YOUTUBE']:
                sample_actors_info['actor'] = row['FRENTES / COLETIVOS']
                sample_actors_info['id'] = ''
                sample_actors_info['username'] = ''
                actors_info.append(sample_actors_info)

    return actors_info
