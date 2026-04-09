from os.path import commonprefix

from contexere.data.context import confirm_rag, confirm_partial_rag

def next_rag(next_group, reference=None):
    rag = next_group
    this_project = next_group[:-5]
    if reference is not None:
        groups = {}
        abbreviations = dict()
        for ref in reference:
            match, project, date, step = confirm_partial_rag(ref)
            if not match:
               raise ValueError(f"Reference '{ref}' is not a partial research artefact group identifier'!")
            if project is None:
                completed_ref = next_group[:-len(ref)] + ref
                project = completed_ref[:-5]
            else:
                completed_ref = ref
            if completed_ref == next_group:
                raise ValueError(f"Reference '{ref}' overlaps with RAG '{next_group}'!")
            if not project in groups:
                groups[project] = list()
            if not completed_ref in groups[project]:
                groups[project].append(completed_ref)
            common = commonprefix([next_group, completed_ref])
            abbreviations[completed_ref] = completed_ref[len(common):]
        tokens = [rag] + concat_abbreviations(groups[this_project], abbreviations)
        del groups[this_project]
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
    fn = next_rag(next_group, reference)
    if keywords is not None:
        fn = "__".join([fn] + keywords)
    return fn + path.suffix

def clone_file(path, next_group, reference=None, keywords=None):
    next_rag = '_'.join(next_group)
    next_filename = '__'.join([next_group,
                               keywords]) + path.suffix
