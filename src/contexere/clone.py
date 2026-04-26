import shutil

from contexere.data.context import confirm_rag, confirm_partial_rag
from contexere.data.groups import ResearchArtefactGroup
from contexere.scheme import join_tokens


def next_rag(next_group, reference=None):
    rag = ResearchArtefactGroup(next_group)
    if reference is not None:
        groups = {}
        abbreviations = dict()
        for ref in reference:
            match, project, date, step = confirm_partial_rag(ref)
            if not match:
               raise ValueError(f"Reference '{ref}' is not a partial research artefact group identifier'!")
            if project is None:
                completed_ref = ResearchArtefactGroup(next_group[:-len(ref)] + ref)
                project = completed_ref.project
            else:
                completed_ref = ResearchArtefactGroup(ref)
            print(completed_ref, rag)
            if completed_ref == rag:
                raise ValueError(f"Reference '{ref}' overlaps with RAG '{next_group}'!")
            if not project in groups:
                groups[project] = list()
            if not completed_ref in groups[project]:
                groups[project].append(completed_ref)
            common = rag.common(completed_ref)
            abbreviations[completed_ref] = str(completed_ref)[len(common):]
        tokens = [str(rag)] + concat_abbreviations(groups[rag.project], abbreviations)
        del groups[rag.project]
        if len(groups) > 0:
            remaining_projects = list(groups.keys())
            print(reference, remaining_projects)
            remaining_projects.sort()
            for p in remaining_projects:
                tokens += concat_abbreviations(groups[p], abbreviations)
        rag = '_'.join(tokens)
    return rag

def concat_abbreviations(rags, abbreviations):
    rags.sort(reverse=True)
    return [abbreviations[r] for r in rags]

def next_filename(path, next_group, reference=None, keywords=None):
    match, project, date, step, remainder = confirm_rag(path.stem)
    if match:
        original_ref = project + date + step
        if reference is None:
            reference = [original_ref]
        else:
            reference += [original_ref]
    fn = str(next_rag(next_group, reference))
    if keywords is not None:
        fn = "__".join([fn] + keywords)
    return fn + path.suffix

def clone_file(path, next_group, reference=None, keywords=None):
    message = f'Cloned from {path.name}.'
    next_rag = join_tokens(next_group, reference)

    if keywords is None:
        keywords = path.stem.split('__')[1:]
    print(next_rag, keywords)
    filename = join_tokens(next_rag, keywords, glue='__') + path.suffix
    new_path = path.parent / filename
    if new_path.exists():
        raise ValueError(f"File '{new_path}' already exists!")
    shutil.copy(path, new_path)
    return new_path, message


