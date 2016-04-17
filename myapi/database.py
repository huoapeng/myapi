from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from myapi import app

engine = create_engine('mysql://root:123@localhost/mydatabase', convert_unicode=True)
# engine = create_engine(app.config['DATABASE_URI'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Model = declarative_base(name='Model')
Model.query = db_session.query_property()

def init_db():
    import myapi.model.user
    Model.metadata.create_all(bind=engine)