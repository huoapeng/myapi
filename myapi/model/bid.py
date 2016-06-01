from myapi import db
from enum import bid_status

bid = db.Table('bid',
    db.Column('user_id', db.Integer, db.ForeignKey('user_model.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task_model.id'), primary_key=True),
    db.Column('bidding_price', db.Integer),
    db.Column('bidding_description', db.Text),
    db.Column('bidding_datatime', db.DateTime)
)