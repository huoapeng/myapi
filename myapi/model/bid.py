
import datetime
from flask import url_for
from myapi import db
from enum import bid_status

class BidModel(db.Model):
    bidding_price = db.Column(db.String(100))
    bidding_description = db.Column(db.Text)
    bidding_timespan = db.Column(db.String(100))
    status = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task_model.id'), primary_key=True)

    user = db.relationship('UserModel', lazy='joined')
    task = db.relationship('TaskModel', lazy='joined')

    def __init__(self, bidding_price=None, bidding_description=None， bidding_timespan=None):
        self.bidding_price = bidding_price
        self.bidding_description = bidding_description
        self.bidding_timespan = bidding_timespan
        self.status = bid_status.start

    def serialize(self):
        return {
            'bidding_price': self.bidding_price,
            'bidding_description': self.bidding_description,
            'bidding_timespan': self.bidding_timespan,
            'status': self.status,
            'user_id': self.user_id,
            'owner': url_for('.userep', _external=True, userid=self.user_id),
            'task_id': self.task_id,
            'task': url_for('.taskep', _external=True, taskid=self.task_id),
        }