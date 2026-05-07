import itertools
import re

from contexere.conf import __GENERATORS__
from contexere.data.interfaces.interpreter import get_execution_context

# Define the scheme with named groups
__pattern__ = re.compile(r'^(?P<project>[a-zA-Z]{2,})'
                         r'(?P<date>[0-9]{2}[o-z][1-9A-V])'
                         r'(?P<step>[a-z])'
                         r'(?:(?:_{1,2}| )(?P<kwds>.+)|_{1,2})?$')
__partial__ = re.compile(r'^(?:(?P<project>[a-zA-Z]{2,})(?=\d))?'
                         r'(?P<date>\d{2}[o-z][1-9A-V]|[o-z][1-9A-V]|[1-9A-V]|)'
                         r'(?P<step>[a-z])$')
__project__ = re.compile(r'^(?P<project>[a-zA-Z]{2,})')


def artefact_name(*keywords, **parameters):
    """
    Build file stem from the filename of the executing script and optional keywords and dictionary items.

    The filename of the executing script is found automatically and broken down into tokens separated by '__'.
    The first token is concatenated with the provided keywords and the key-value pairs of the dictionary
    using '__' as separator.

    Whitespaces of keywords are replaced by underscores '_'.

    Whitespaces of keys or values are removed. Key-value pairs are concatenated by an underscore '_'.
    """
    _, name = get_execution_context()
    notebookID = name.split('__')[0]

    file_stem = '__'.join([notebookID] +
                         [str(k).replace(' ', '_') for k in keywords] +
                         [str(key).replace(' ', '') + '_' + str(value).replace(' ', '')
                          for key, value in parameters.items()])
    return file_stem

def confirm_rag(token, pattern=__pattern__):
    match = pattern.match(token)
    if match:
        project = match.group('project')
        date = match.group('date')
        step = match.group('step')
        remainder = match.group('kwds')
    else:
        project, date, step, remainder = None, None, None, None
    return match, project, date, step, remainder

def confirm_partial_rag(token, pattern=__partial__):
    match = pattern.match(token)
    if match:
        project = match.group('project')
        date = match.group('date')
        step = match.group('step')
    else:
        project, date, step = None, None, None
    return match, project, date, step

def confirm_project_identifier(token, pattern=__project__):
    match = pattern.match(token)
    if match:
        project = match.group('project')
    else:
        project = None
    return match, project

def index_file_artefact(db, filepath, project, date, step, remainder):
    project_id = db.upsert('Project', dict(Name=project))
    rag_id = db.upsert('RAG', dict(ID=project + date + step,
                                   Project=project, Date=date, Step=step))
    if remainder is not None:
        keywords = index_dependencies(db, rag_id, remainder)
        keyword_dict = index_keywords(db, rag_id, keywords)
    else:
        keyword_dict = {}
    path_id = db.upsert('Path', dict(Name=str(filepath.parents[0])))
    artefact_id = db.insert('Artefact', dict(RAG=rag_id,
                                             FileName=filepath.name, FileExtension=filepath.suffix,
                                             Path=path_id,
                                             IsGenerator=filepath.suffix in __GENERATORS__,
                                             IsDirectory=filepath.is_dir())
                            )
    return dict(project_id=project_id, rag_id=rag_id,
                artefact_id=artefact_id, path_id=path_id, keyword_dict=keyword_dict)

def index_dependencies(db, rag_id, remainder):
    keywords = list()
    parse_dependencies = True
    tokens = list(remainder.split('_'))
    while parse_dependencies and len(tokens) > 0:
        token = tokens.pop(0)
        match, par_project, par_date, par_step = confirm_partial_rag(token)
        if match:
            if par_project is None or par_date is None:
                match, par_project, par_date, par_step = confirm_partial_rag(rag_id[:-len(token)] + token)
            parent_id = db.upsert('RAG', dict(ID=par_project + par_date + par_step,
                                              Project=par_project, Date=par_date, Step=par_step))
            kg_id = db.upsert('KnowledgeGraph', dict(Parent=parent_id, Child=rag_id))
        else:
            parse_dependencies = False
            keywords.append(token)
    keywords += tokens
    return keywords

def index_keywords(db, rag_id, keywords):
    keyword_ids = []
    keyword_index = []
    keyvalue_ids = []
    if '' in keywords:  # potential key-value pairs
        for first, second in itertools.pairwise(keywords):
            if first == '':
                continue
            kwd_id = upsert_keyword(db, first, keyword_ids, keyword_index, rag_id)
            try:
                val = float(second)
                is_numeric = True
            except ValueError:
                is_numeric = False
            if second != '':  # key_value pair
                keyvalue_index_id = db.insert('KeyValueIndex',
                                         dict(RAG=rag_id, Keyword=kwd_id, Value=second, IsNumeric=is_numeric))
                keyvalue_ids.append(keyvalue_index_id)
    else:
        for kwd in keywords:
            kwd_id = upsert_keyword(db, kwd, keyword_ids, keyword_index, rag_id)
    return keyword_ids, keyword_index, keyvalue_ids


def upsert_keyword(db, first, keyword_ids, keyword_index, rag_id):
    kwd_id = db.upsert('Keyword', dict(Keyword=first))
    kwd_index_id = db.insert('KeywordIndex', dict(RAG=rag_id, Keyword=kwd_id))
    keyword_ids.append(kwd_id)
    keyword_index.append(kwd_index_id)
    return kwd_id


def clean_up_remainder(remainder):
    """
    The remainder is the tail of a filename stem after the first underscore.
    It might contain references, which might have to be removed.
    """
    parse_dependencies = True
    tokens = list(remainder.split('__'))
    keywords = list()
    while len(tokens) > 0:
        token = tokens.pop(0)
        if len(token) > 0:
            if parse_dependencies:
                match, par_project, par_date, par_step = confirm_partial_rag(token.split('_')[0])
                if match:
                    continue
                else:
                    parse_dependencies = False
            keywords.append(token)
    return '__'.join(keywords)

if __name__ == '__main__':
    from pathlib import Path
    from contexere.data.interfaces.contextdb import ContextDB

    in_memory_db = ContextDB(path='')
    in_memory_db.create_tables()
    index_file_artefact(in_memory_db, Path.home() / 'ERP26pBa_9b__example__value_1.txt',
                        'ERP', '26pB', 'a', '9b__example__value_1.txt')
    index_file_artefact(in_memory_db, Path.home() / 'ERP26pBa_example',
                        'ERP', '26pB', 'a', 'example')