from core.output import FileOutput
from server.api_exceptions import InvalidUsage
from server.models import db
from flask import Flask, jsonify
from server.models import Actor
import json
import os

app = Flask(__name__)
bank_connection = 'postgresql://postgres:trisha@localhost/youtube_database'
app.config['SQLALCHEMY_DATABASE_URI'] = bank_connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


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


@app.route('/dates', methods=['GET'])
def list_dates():
    dates = db.session.query(Actor.collected_date).distinct()
    all_dates = [item[0] for item in dates]

    return jsonify({'dates': all_dates})


@app.route('/<date>/canal/<actor>/videos', methods=['GET'])
def list_actor_videos_info(date, actor):
    data_folders = [x[1] for x in os.walk('data/')][0]

    raise_date_error, raise_actor_error = True, True
    list_actors_video_info = {'videos': []}

    if date == 'latest':
        data_folders.sort()
        folder = data_folders[-1]
        date_file = 'data/'+folder+'/channel_videos/'
        raise_date_error = False
    else:
        for folder in data_folders:
            check_folder = folder.split('_')[0]
            if date == check_folder:
                date_file = 'data/'+folder+'/channel_videos/'
                raise_date_error = False

    if raise_date_error:
        raise InvalidUsage("Date was mistyped or our database didn't collected"
                           " data in this date. Try a date in this format"
                           " day-month-year, e.g. 07-05-2018 or try list the"
                           " dates that our system collected data at"
                           " youtube-data-monitor.herokuapp.com/dates.",
                           status_code=450)

    actor = actor.replace('_', ' ')
    data_folders = list(os.walk(date_file))[0][2]
    for folder in data_folders:
        if folder.replace('.csv', '').lower() == actor.lower():
            actor_videos_info = FileOutput(date_file+folder).get_all_data()
            list_actors_video_info['videos'] = actor_videos_info
            raise_actor_error = False

    if raise_actor_error:
        raise InvalidUsage("Actor name was mistyped or this actor name don't"
                           " exist in our database. Try list all the actors at"
                           " youtube-data-monitor.herokuapp.com/actors.",
                           status_code=460)

    return jsonify(list_actors_video_info)


@app.route('/<date>/canal/<actor>', methods=['GET'])
def list_actor_channel_info(date, actor):

    raise_date_error, raise_actor_error = True, True
    dates = db.session.query(Actor.collected_date).distinct()
    all_dates = [item[0] for item in dates]

    if date == 'latest':
        all_dates.sort()
        given_date = all_dates[-1]
        raise_date_error = False
    else:
        for item in all_dates:
            if date == item:
                raise_date_error = False

    if raise_date_error:
        raise InvalidUsage("Date was mistyped or our database didn't collected"
                           " data in this date. Try a date in this format"
                           " day-month-year, e.g. 07-05-2018 or try list the"
                           " dates that our system collected data at"
                           " youtube-data-monitor.herokuapp.com/dates.",
                           status_code=450)

    actor = actor.replace('_', ' ')
    actor_info = db.session.query(Actor).filter_by(actor_name=actor).first()
    if actor_info is not None:
        raise_actor_error = False

    if raise_actor_error:
        raise InvalidUsage("Actor name was mistyped or this actor name don't"
                           " exist in our database or"
                           " there is no data to provide for this actor."
                           " Try list all the actors at"
                           " youtube-data-monitor.herokuapp.com/actors.",
                           status_code=460)

    del actor_info.__dict__['_sa_instance_state']
    return jsonify(actor_info.__dict__)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
