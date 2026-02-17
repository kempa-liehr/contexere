from contexere import conf
from contexere.data.context import confirm_rag, index_file_artefact, index_note_artefact
import contexere.data.interfaces.contextdb as cdb

def init_cache(path, db):
    fill_cache(path, db)
    return db

def fill_cache(db, root='/', notes=['org, md']):
    db.create_tables()
    for path in root.rglob('*'):
        match, project, date, step, keywords = confirm_rag(path.name)
        if match:
            index_file_artefact(db, path, project, date, step, keywords)
        elif path.suffix in notes and not path.is_dir():
            raise NotImplementedError


if __name__ == '__main__':
    db = cdb.ContextDB(path='')
    db.create_tables()