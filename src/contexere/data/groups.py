"""
Classes supporting the naming scheme.
"""
from contexere.data.context import confirm_rag, confirm_partial_rag
from contexere.scheme import decode_abbreviated_datetime


class ResearchArtefactGroup:
    def __init__(self, identifier):
        self._frozen = False
        match, self.project, self.date, self.step, self.remainder = confirm_rag(identifier)
        if not match:
            raise ValueError(f"Reference '{identifier}' is not a research artefact group identifier.")
        else:
            self.identifier_ = identifier
        self.iso_date = decode_abbreviated_datetime(self.date)
        self.year = self.iso_date.year
        self.month = self.iso_date.month
        self.day = self.iso_date.day
        self._frozen = True

    def __setattr__(self, name, value):
        if getattr(self, "_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} is immutable")
        super().__setattr__(name, value)

    def __str__(self):
        return self.identifier_

    def __lt__(self, other):
        return self.identifier_ < other.identifier_

    def __gt__(self, other):
        return self.identifier_ > other.identifier_

    def __eq__(self, other):
        return self.identifier_ == other.identifier_

    def __hash__(self):
        return id(self.identifier_)

    def common(self, other):
        if type(other) == str:
            other_group = ResearchArtefactGroup(other)
        else:
            other_group = other
        common = ''
        if self.project == other_group.project:
            common += self.project
            if self.year == other_group.year:
                common += self.date[:2]
                if self.month == other_group.month:
                    common += self.date[2]
                    if self.day == other_group.day:
                        common += self.date[3]
                        if self.step == other_group.step:
                            common += self.step
        return common


def compile_references(next_rag, references):
    rag = ResearchArtefactGroup(next_rag)
    same_project = []
    other_projects = {}
    for ref in references:
        match, par_project, par_date, par_step = confirm_partial_rag(ref)
        if match:
            if par_project is None or par_date is None:
                match, par_project, par_date, par_step = confirm_partial_rag(rag.identifier_[:-len(ref)] + ref)
        if match is None:
            raise ValueError(f'Reference `{ref}` is neither a full '
                             'nor a partial research artefact group identifier!')
        rag_ref = ResearchArtefactGroup(par_project + par_date + par_step)
        if rag.project == rag_ref.project:
            same_project.append(rag_ref)
        elif rag_ref.project in other_projects:
            other_projects[rag_ref.project].append(rag_ref)
        else:
            other_projects[rag_ref.project] = [rag_ref]
    same_project.sort(reverse=True)
    abbreviate_refs = []
    for rag_ref in same_project:
        if rag == rag_ref or rag < rag_ref:
            raise ValueError(f'RAG `{rag}` was created before reference `{rag_ref}`!')
        abbreviate_refs.append(rag_ref.identifier_[len(rag.common(rag_ref)):])
    other_project_identifier = list(other_projects.keys())
    other_project_identifier.sort()
    for project in other_project_identifier:
        other_projects[project].sort(reverse=True)
        first_rag = other_projects[project].pop(0)
        if rag.iso_date < first_rag.iso_date:
            raise ValueError(f'RAG `{rag}` was created before reference `{first_rag}`!')
        abbreviate_refs.append(first_rag.identifier_)
        for rag_ref in other_projects[project]:
            if rag.iso_date < rag_ref.iso_date:
                raise ValueError(f'RAG `{rag}` was created before reference `{rag_ref}`!')
            abbreviate_refs.append(first_rag.identifier_[len(first_rag.common(rag_ref)):])
    return abbreviate_refs

if __name__ == '__main__':
    compile_references('ERP26s5b', ['a', 'r4b', 'BBC26s5a', 'ABC26s6a'])