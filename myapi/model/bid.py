
import datetime
from flask import url_for
from myapi import db
from enum import bid_status

class BidModel(db.Model):
    price = db.Column(db.String(100))
    description = db.Column(db.Text)
    timespan = db.Column(db.String(100))
    status = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'), primary_key=True)

    user = db.relationship('UserModel', lazy='joined')
    project = db.relationship('ProjectModel', lazy='joined')

    def __init__(self, bidding_price=None, bidding_description=None, bidding_timespan=None):
        self.bidding_price = bidding_price
        self.bidding_description = bidding_description
        self.bidding_timespan = bidding_timespan
        self.status = bid_status.start

    def serialize(self):
        return {
            'price': self.price,
            'description': self.description,
            'timespan': self.timespan,
            'status': self.status,
            'userid': self.user_id,
            'user': url_for('.user', _external=True, userid=self.user_id),
            'projectid': self.project_id,
            'project': url_for('.project', _external=True, projectid=self.project_id),
        }