from server.api_exceptions import InvalidUsage
from server.queries import DBYouTube
from flask import Flask, jsonify
import os
from server import app, db


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/actors', methods=['GET'])
def list_actors():
    list_actors_original = DBYouTube.get_all_actors_name()

    return jsonify(list_actors_original)


@app.route('/dates', methods=['GET'])
def list_dates():

    return jsonify(DBYouTube.get_dates())


@app.route('/<date>/canal/<actor>/videos', methods=['GET'])
def list_actor_videos_info(date, actor):

    raise_date_error, raise_actor_error = True, True
    db_date = date_latest(date)
    raise_date_error = db_date is None

    if raise_date_error:
        raise InvalidUsage("Date was mistyped or our database didn't collected"
                           " data in this date. Try a date in this format"
                           " day-month-year, e.g. 07-05-2018 or try list the"
                           " dates that our system collected data at"
                           " youtube-data-monitor.herokuapp.com/dates.",
                           status_code=450)

    actor = actor.replace('_', ' ')

    result_actor = DBYouTube.get_info_actor(db_date, actor)
    raise_actor_error = result_actor is None
    if raise_actor_error:
        raise InvalidUsage("Actor name was mistyped or this actor name don't"
                           " exist in our database or"
                           " there is no data to provide for this actor."
                           " Try list all the actors at"
                           " youtube-data-monitor.herokuapp.com/actors.",
                           status_code=460)

    all_videos = DBYouTube.get_actor_videos(db_date,
                                            result_actor['channel_id'])
    return jsonify({'videos': all_videos})


@app.route('/<date>/canal/<actor>', methods=['GET'])
def list_actor_channel_info(date, actor):

    raise_date_error, raise_actor_error = True, True
    db_date = date_latest(date)
    raise_date_error = db_date is None

    if raise_date_error:
        raise InvalidUsage("Date was mistyped or our database didn't collected"
                           " data in this date. Try a date in this format"
                           " day-month-year, e.g. 07-05-2018 or try list the"
                           " dates that our system collected data at"
                           " youtube-data-monitor.herokuapp.com/dates.",
                           status_code=450)

    actor = actor.replace('_', ' ')
    result_actor = DBYouTube.get_info_actor(db_date, actor)
    raise_actor_error = result_actor is None

    if raise_actor_error:
        raise InvalidUsage("Actor name was mistyped or this actor name don't"
                           " exist in our database or"
                           " there is no data to provide for this actor."
                           " Try list all the actors at"
                           " youtube-data-monitor.herokuapp.com/actors.",
                           status_code=460)

    return jsonify(result_actor)


def date_latest(date):
    all_dates = DBYouTube.get_dates()['dates']
    raise_date_error = True
    if date == 'latest':
        return all_dates[0]
    else:
        for item in all_dates:
            if date == item:
                return date
    return None


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
