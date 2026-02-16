import re

from contexere.conf import __GENERATORS__

# Define the scheme with named groups
__pattern__ = re.compile(r'^(?P<project>[a-zA-Z]+)(?P<date>[0-9]{2}[o-z][1-9A-V])(?P<step>[a-z]+)(?:_+(?P<kwds>.+))?_*')
__partial__ = re.compile(r'^(?P<project>[A-Za-z]+(?=\d))?(?P<date>(?:\d{2}[o-z][1-9A-V]|[o-z][1-9A-V]|[1-9A-V])?)(?P<step>[a-z]{1,2})$')
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
def index_file_artefact(db, filepath, project, date, step, remainder, user):
    project_id = db.upsert('Project', dict(Name=user))
    researcher_id = db.upsert('Researcher', dict(Name=user))
    rag_id = db.upsert('RAG', dict(Project=project, Date=date, Enumerate=step, ResearcherID=researcher_id))
    keywords = index_dependencies(db, rag_id, remainder)
    path_id = db.upsert('Path', dict(Name=filepath.parents[0]))
    artefact_id = db.insert('Artefact', dict(RAG=rag_id,
                                             Filename=filepath.name, FileExtension=filepath.suffix,
                                             Path=path_id,
                                             IsGenerator=filepath.suffix in __GENERATORS__,
                                             IsADirectory=filepath.is_dir())
                            )
    keyword_dict = index_keywords(db, rag_id, keywords, remainder)
    return dict(project_id=project_id, researcher_id=researcher_id, rag_id=rag_id,
                artefact_id=artefact_id, path_id=path_id, keyword_dict=keyword_dict)

def index_dependencies(db, rag_id, remainder):
    keywords = list()
    for token in remainder.split('_'):
        match, par_project, par_date, par_step = confirm_partial_rag(token)
        if match:
            if par_project is not None:
                # It is not clear if this dependency is from the researcher, who generated the original file.
                parent_id = db.upsert('RAG', dict(Project=par_project, Date=par_date, Enumerate=par_step))
            else:
                match, par_project, par_date, par_step = confirm_rag(rag_id[:-len(token)] + token)
                parent_id = db.upsert('RAG', dict(Project=par_project, Date=par_date, Enumerate=par_step))
            kg_id = db.upsert('KnowledgeGraph', dict(Parent=parent_id, Child=rag_id))
        else:
            keywords.append(token)
    return keywords

def index_keywords(db, rag_id, keywords, remainder):
    pass

def index_note_artefact(path, filename, markup='org'):
    pass
