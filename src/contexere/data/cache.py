from contexere.conf import __IGNORE__
from contexere.data.context import confirm_rag, index_file_artefact
import contexere.data.interfaces.contextdb as cdb

def exclude_path(path, ignore=__IGNORE__):
    exclude = any([path.match(pattern) for pattern in ignore])
    return exclude

def fill_cache(db, root='/'):
    db.create_tables()
    for path in root.rglob('*'):
        if not exclude_path(path):
            match, project, date, step, keywords = confirm_rag(path.name)
            if match:
                try:
                    index_file_artefact(db, path, project, date, step, keywords)
                except:
                    print(path)


if __name__ == '__main__':
    db = cdb.ContextDB(path='')
    db.create_tables()
