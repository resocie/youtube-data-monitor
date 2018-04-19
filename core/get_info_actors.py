from youtube.youtube import YoutubeAPI
import csv

class get_actors_info:

    def __init__(self):
        self.user = YoutubeAPI()

    def read_actors_info(self):
        with open('data/grupos_politicos.csv', 'r') as csvfile:
            readCSV = csv.DictReader(csvfile)
            actors_dict = []
            for row in readCSV:
                aux_dict = {'ator': '', 'username': '', 'id': ''}
                if 'https' in row['YOUTUBE']:
                    aux_dict['ator'] = row['FRENTES / COLETIVOS']
                    if 'user' in row['YOUTUBE']:
                        url = row['YOUTUBE'].split('/')
                        index = url.index('user') + 1
                        aux_dict['username'] = url[index]
                        aux_dict['id'] = ''
                    elif 'channel' in row['YOUTUBE']:
                        url = row['YOUTUBE'].split('/')
                        index = url.index('channel') + 1
                        aux_dict['id'] = url[index]
                        aux_dict['username'] = ''
                    actors_dict.append(aux_dict)
                elif 'S/' in row['YOUTUBE']:
                    aux_dict['ator'] = row['FRENTES / COLETIVOS']
                    aux_dict['id'] = ''
                    aux_dict['username'] = ''
                    actors_dict.append(aux_dict)
        self._insert_actor_info(actors_dict)

    def _insert_actor_info(self, actors_dict):
        check = self.user.generate_csv()
        if check:
            for item in actors_dict:
                if item['username']:
                    result = self.user.get_channel_info_by_username(item['username'])
                    item['id'] = result['items'][0]['id']
                self.user.insert_data(param = 'channel_id',
                            value = item['id'],
                            field_name = 'ator',
                            field_value = item['ator'].replace('\n', ''))
                self.user.insert_data(param = 'username',
                            value = item['username'],
                            field_name = 'ator',
                            field_value = item['ator'].replace('\n', ''))
