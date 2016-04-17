from sqlalchemy import Column, Integer, String
from myapi.database import Model

class User(Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(50), , default=0)


    def __init__(self, email=None, password=None):
        self.nickname = email
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.nickname)