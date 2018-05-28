from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Actor(db.Model):
    actor_name = db.Column(db.Text)
    subscribers = db.Column(db.Integer)
    video_count = db.Column(db.Integer)
    title = db.Column(db.Text)
    channel_id = db.Column(db.String(30), primary_key=True)
    view_count = db.Column(db.Integer)
    collected_date = db.Column(db.String(10), primary_key=True)
    comment_count = db.Column(db.Integer)
    thumbnail_url = db.Column(db.Text)
    description = db.Column(db.Text)
    keywords = db.Column(db.Text)
    banner_url = db.Column(db.Text)
    above_one_hundred_thousand = db.Column(db.Boolean)

    def __init__(self, actor_name, subscribers, video_count, title,
                 channel_id, view_count, collected_date,
                 comment_count, thumbnail_url, description,
                 keywords, banner_url, above_one_hundred_thousand):

        self.actor_name = actor_name
        self.subscribers = subscribers
        self.video_count = video_count
        self.title = title
        self.channel_id = channel_id
        self.view_count = view_count
        self.collected_date = collected_date
        self.comment_count = comment_count
        self.thumbnail_url = thumbnail_url
        self.description = description
        self.keywords = keywords
        self.banner_url = banner_url
        self.above_one_hundred_thousand = above_one_hundred_thousand

    def __repr__(self):
        return 'id-{}'.format(self.channel_id)
