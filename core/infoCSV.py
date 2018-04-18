from youtube.youtube import YoutubeAPI
import csv

def readActors():
    with open('../data/grupos_politicos.csv', 'r') as csvfile:
        readCSV = csv.DictReader(csvfile)
        actors_dict = []
        for row in readCSV:
            dict = {}
            if 'https' in row['YOUTUBE']:
                dict['ator'] = row['FRENTES / COLETIVOS']
                if 'user' in row['YOUTUBE']:
                    url = row['YOUTUBE'].split("/")
                    index = url.index("user") + 1
                    dict['username'] = url[index]
                    dict['id'] = ''
                elif 'channel' in row['YOUTUBE']:
                    url = row['YOUTUBE'].split("/")
                    index = url.index("channel") + 1
                    dict['id'] = url[index]
                    dict['username'] = ''
                actors_dict.append(dict)
            elif 'S/' in row['YOUTUBE']:
                dict['ator'] = row['FRENTES / COLETIVOS']
                dict['id'] = ''
                dict['username'] = ''
                actors_dict.append(dict)

        return actors_dict

    check = generate_csv()

    if check:
        actors_dict = readActors()
        for item in actors_dict:
            if item['username'] != '':
                result = get_channel_info(item['username'])
                item['id'] = result['items'][0]['id']
            insert_data(param = 'channel_id',
                        value = item['id'],
                        field_name = 'ator',
                        field_value = item['ator'])
            insert_data(param = 'username',
                        value = item['username'],
                        field_name = 'ator',
                        field_value = item['ator'])
