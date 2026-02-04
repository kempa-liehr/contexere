"""
Discover files following the naming convention
"""

from pathlib import Path

import pandas as pd

from contexere import __pattern__ as pattern


# Function to group files by common project and date
def build_context(directory='.', project_filter=None):
    context = dict()
    timeline = dict()

    # Iterate over files and directories in the specified folder
    for path in Path(directory).iterdir():
        match = pattern.match(path.name)
        if match:
            project = match.group('project')
            date = match.group('date')
            step = match.group('step')
            if project_filter is None or project == project_filter:
                grow_context(context, project, date, step, path)
                extend_timeline(timeline, date, path, project, step)
    return context, timeline


def extend_timeline(timeline, date, path, project, step):
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
                 path: Path):
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


def summary(directory='.', buffered_context=None):
    if buffered_context is None:
        context, _ = build_context(directory)
    else:
        context = buffered_context
    summary_dict = dict()
    for project, dates_dict in context.items():
        last_date = max(dates_dict.keys())
        last_step = max(dates_dict[last_date].keys())
        unique_rai = 0
        total_project_files = 0
        for steps_dict in dates_dict.values():
            unique_rai += 1
            total_project_files += sum([len(file_list) for file_list in steps_dict.values()])

        summary_dict[project] = pd.Series({'RAI': unique_rai,
                                           'Files': total_project_files,
                                           'Latest': last_date + last_step})
    summary_df = pd.DataFrame(summary_dict).transpose()
    summary_df.columns.name = 'Project'
    summary_df.sort_values(by=['Latest'], ascending=False, inplace=True)

    if len(summary_df) == 0:
        raise ValueError('No context found in folder "{}".'.format(str(directory)))
    return summary_df


if __name__ == "__main__":
    summary()