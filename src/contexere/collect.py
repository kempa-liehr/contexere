"""
Discover files following the naming convention
"""

from pathlib import Path

import pandas as pd

from contexere import __pattern__ as pattern


# Function to group files by common project and date
def build_context(directory='.', project_filter='', recursive=False):
    """
    Build context of grouped research artefacts over projects and time.

    Args:
        directory: Folder to search for research artefacts (default='.')
        project_filter: Starting letters of project identifier
                        (default='' finds all files following the naming convention)
        recursive: Traverse directory tree recursively (default=False)

    Returns:
        (context_dict, timeline_dict)
    """
    context = dict()
    timeline = dict()

    if recursive:
        file_iterator = Path(directory).rglob(project_filter + '*')
    else:
        file_iterator = Path(directory).glob(project_filter + '*')
    # Iterate over files and directories in the specified folder
    for path in file_iterator:
        match = pattern.match(path.name)
        if match:
            project = match.group('project')
            date = match.group('date')
            step = match.group('step')
            grow_context(context, project, date, step, path)
            extend_timeline(timeline, date, project, step, path)
    return context, timeline


def extend_timeline(timeline: dict[str, dict[str, dict[str, list[Path]]]],
                    date: str,
                    project: str,
                    step: str,
                    path: Path) -> None:
    """
        Add file to timeline dictionary.

        Append the path of a research artefact identified by its `date`, `project`, and `step` to the
        `timeline` dictionary.

        Args:
            timeline: Timeline dictionary to be appended with path to research artefact.
            date: Date abbreviation
            project: Project identifier
            step: Lower case characters counting the research artefacts for a specific `date`
            path: Path to the research artefact

        Returns:
            None
        """
    if not date in timeline:
        timeline[date] = dict()
    if not project in timeline[date]:
        timeline[date][project] = dict()
    if not step in timeline[date][project]:
        timeline[date][project][step] = list()
    timeline[date][project][step].append(path)


def grow_context(context: dict[str, dict[str, dict[str, list[Path]]]],
                 project: str,
                 date: str,
                 step: str,
                 path: Path) -> None:
    """
    Add file to context dictionary.

    Append the path of a research artefact identified by its `project`, `date`, and `step` to the `context` dictionary.

    Args:
        context: Context dictionary to be appended with path to research artefact.
        project: Project identifier
        date: Date abbreviation
        step: Lower case characters counting the research artefacts for a specific `date`
        path: Path to the research artefact

    Returns:
        None
    """
    if not project in context:
        context[project] = dict()
    if not date in context[project]:
        context[project][date] = dict()
    if not step in context[project][date]:
        context[project][date][step] = list()
    context[project][date][step].append(path)


def summary(directory='.', buffered_context=None, project_filter='', recursive=False):
    """
    Summarise context as pandas.DataFrame with columns 'RAGs, 'Files', 'Latest' and index given by project identifiers.
    The rows are sorted according to column 'Latest'.

    Args:
        directory: Folder to search for research artefacts (default='.')
        buffered_context: context_dictionary, which already has been collected (default=None)
        project_filter: Starting letters of project identifier
                        (default='' finds all files following the naming convention)
        recursive: Traverse directory tree recursively (default=False)

    Returns:
        pd.DataFrame with columns 'RAGs', 'Files', 'Latest' and index given by project identifiers.
    """
    if buffered_context is None:
        context, _ = build_context(directory, project_filter, recursive)
    else:
        context = buffered_context
    summary_dict = dict()
    for project, dates_dict in context.items():
        last_date = max(dates_dict.keys())
        last_step = max(dates_dict[last_date].keys())
        unique_ragi = 0
        total_project_files = 0
        for steps_dict in dates_dict.values():
            unique_ragi += 1
            total_project_files += sum([len(file_list) for file_list in steps_dict.values()])

        summary_dict[project] = pd.Series({'RAGs': unique_ragi,
                                           'Files': total_project_files,
                                           'Latest': last_date + last_step})
    summary_df = pd.DataFrame(summary_dict).transpose()
    summary_df.columns.name = 'Project'

    if len(summary_df) == 0:
        raise ValueError('No context found in folder "{}".'.format(str(directory)))
    else:
        summary_df.sort_values(by=['Latest'], ascending=False, inplace=True)
    return summary_df


if __name__ == "__main__":
    summary()