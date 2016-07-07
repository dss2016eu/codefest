#! coding:utf-8
__author__ = 'kassandracharalampidou'

from model import EuroTweet
from helpers import safe_session, autoconnect
import sqlalchemy as sa

DB_NAME = 'DATABASE_LOCAL'


class DBManagerFactory():
    def __init__(self, settings, rds_name, db_name=None):
        self.settings = settings
        self.rds_name = rds_name
        self.db_name = db_name
        if self.db_name is None:
            self.db_name = settings.get(rds_name, 'default_db')

    def get_manager(self):
        engine, session = autoconnect(dict(self.settings.items(self.rds_name)), self.db_name)
        return GlobalDBManager(session, engine)


class AbstractDBManager():
    '''
    Manages queries from the db and injects results to procedures that need them
    '''
    @safe_session
    def __init__(self, session, engine):
        self.session = session
        self.engine = engine

    def db_flush(self):
        self.session.flush()

    def db_commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
        self.engine.dispose()


class GlobalDBManager(AbstractDBManager):
    def get_euro_tweets_geo_by_date(self, date_filters):
        geo = self.session.query(EuroTweet).filter(
        sa.and_(EuroTweet.date >= date_filters[0], EuroTweet.date < date_filters[1])).limit(40000)
        return geo

    def get_euro_tweets_geo_by_tag(self, tag):
        print tag
        print tag[2]
        geo = self.session.query(EuroTweet).filter(sa.or_(EuroTweet.text.like("%"+tag[0]+"%"))).all()
        return geo

    def get_euro_tweets_geo_by_language(self, language):
        geo = self.session.query(EuroTweet).filter(EuroTweet.lang.__eq__(language)).limit(10000)
        return geo