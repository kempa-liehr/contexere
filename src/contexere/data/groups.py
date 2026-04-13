"""
Classes supporting the naming scheme.
"""
from contexere.data.context import confirm_rag
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