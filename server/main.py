from core.output import FileOutput
from server.api_exceptions import InvalidUsage
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/actors', methods=['GET'])
def list_actors():
    with open('data/actors.json') as data_file:
        list_actors_original = json.load(data_file)

    return jsonify(list_actors_original)


@app.route('/<date>/canal/<actor>', methods=['GET'])
def list_actor_channel_info(date, actor):
    data_folders = [x[1] for x in os.walk('data/')][0]

    raise_date_error, raise_actor_error = True, True

    for folder in data_folders:
        check_folder = folder.split('_')[0]
        if date == check_folder:
            date_file = 'data/'+folder+'/youtube.csv'
            raise_date_error = False

    if raise_date_error:
        raise InvalidUsage("Date was mistyped or our database didn't colleted"
                           "data in this date. Try a date in this format "
                           "day-month-year, e.g. 07-05-2018.", status_code=450)

    try:
        actor = actor.replace('_', ' ')
        actor_info = FileOutput(date_file).get_row(column='actor', value=actor)
        if actor_info:
            actor_info['actor'] = actor
            raise_actor_error = False
    except ValueError:
        raise_actor_error = True

    if raise_actor_error:
        raise InvalidUsage("Actor name mistyped or this actor name don't "
                           "exist in our database. Try list all the actors in "
                           "youtube-data-monitor.herokuapp.com/actors.",
                           status_code=460)

    return jsonify(actor_info)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
