import shutil
import subprocess

from contexere.data.context import confirm_partial_rag, confirm_rag
from contexere.data.groups import ResearchArtefactGroup, compile_references
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

def add_to_git_repository(path, message):
    try:
        repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                            cwd=path.parent, stderr=subprocess.DEVNULL, text=True,
                                            ).strip()
    except subprocess.CalledProcessError:
        output = f'Cloned file {path} is not inside a git repository.'
    else:
        subprocess.check_call(["git", "add", str(path.relative_to(repo_root))],
                              cwd=repo_root)
        subprocess.check_call(["git", "commit", "-m", message],
                              cwd=repo_root)
        output = f'Added cloned file {path} to git repository.'
    return output

def clone_file(path, next_group, references=None, keywords=None):
    message = f'Cloned from {path.name}.'
    if references is None:
        next_rag = next_group
    else:
        if type(references) == str:
            compiled_references = compile_references(next_group, [references])
        else:
            compiled_references = compile_references(next_group, references)
        next_rag = join_tokens(next_group, compiled_references)

    if keywords is None:
        keywords = path.stem.split('__')[1:]
    filename = join_tokens(next_rag, keywords, glue='__') + path.suffix
    new_path = path.parent / filename
    if new_path.exists():
        raise ValueError(f"File '{new_path}' already exists!")
    shutil.copy(path, new_path)

    output = add_to_git_repository(new_path, message)

    return new_path, output


