import os
from sqlalchemy import inspect, insert

from contexere import conf
import contexere.data.interfaces.contextdb as cdb

def init_cache(path, db):
    fill_cache(path, db)
    return db

def init_researcher_table(db, user=conf.username):
    if len(db.get_researchers()) == 0:
        stmt = insert(cdb.researcher).values(Name=user)
        db.connect()
        db.connection.execute(stmt)
        result = db.connection.commit()
    else:
        result = None
    return result

def fill_cache(db, path='/'):
    db.create_tables()
    init_researcher_table(db)

if __name__ == '__main__':
    db = cdb.ContextDB(path='')
    db.create_tables()
    result = init_researcher_table(db)
    print(db.get_researchers())