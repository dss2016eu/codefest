#! coding:utf-8
'''
'''

import sqlalchemy as sa
import re
import traceback

from copy import copy
from sqlalchemy.orm import sessionmaker

dbname_ptn = re.compile('.*(?=/)/([\w]+)')

_CONNECTIONS = {}

class DictWrapper:
    def __init__(self, entries):
        self.__dict__.update(entries)


def autoconnect(rds_cred, db_name=None):
    '''
    Returns engine and session
    '''
    e = get_engine(rds_cred, database=db_name)
    if (db_name in _CONNECTIONS.keys()):
        s = _CONNECTIONS[rds_cred['host'], db_name]
    else:
        s = sessionmaker(bind=e)()
        _CONNECTIONS[rds_cred['host'], db_name] = s
    return e, s


def get_engine(rds_cred, config=None, database=None, **kwargs):
    '''
    Initialize engine to db
    '''
    constr = '%(driver)s://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'
    if config:
        constr = constr % config
    elif database:
        #cnf = copy(dict(settings.items('DATABASE')))
        cnf = copy(rds_cred)
        cnf['database'] = database
        constr = constr % cnf
    else:

        constr = constr % rds_cred

    engine = sa.create_engine(constr, **kwargs)
    return engine


def safe_session(func):
    '''
    wrap function, check first arg should be session otherwise gets second argument
      if string -> ups connection,
         if error raise -> dispose connection
    '''
    def wrapper(*args, **kwargs):
        '''
        If receive as session real SqlAlchemy session name, just calls func
        and wraps it fails,
        If receive string, connect to db, wraps, and ispose connect after end
        '''
        is_nested = False
        cls_name = lambda x: type(x).__name__

        session = args[1] if cls_name(args[0])not in ('SessionMaker', 'ScopedSession')else args[0]

        if cls_name(session) in ('SessionMaker', 'ScopedSession'):
            is_nested = True
        elif isinstance(session, basestring):
            engine, session = autoconnect(session)
        else:
            raise Exception('Unknown type as session param %s' % cls_name(session))

        #ret_value = func(session, *args, **kwargs)
        try:
            ret_value = func(*args, **kwargs)
        except Exception as e:
            session.rollback()
            del session
            if not is_nested:
                engine.dispose()
                del engine
            s = traceback.format_exc()
            raise
        else:
            session.commit()
            session.close_all()
            del session
            if not is_nested:
                engine.dispose()
                del engine

        return ret_value

    return wrapper