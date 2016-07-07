#! coding:utf-8

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EuroTweet(Base):
    __tablename__ = 'behagunea_euro_tweets'

    mention_id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.Date, nullable=False)
    geoinfo = sa.Column(sa.String(length=50), nullable=False)
    lang = sa.Column(sa.String(length=50), nullable=False)
    text = sa.Column(sa.String(length=50), nullable=False)