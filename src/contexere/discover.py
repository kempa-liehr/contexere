"""
Discover files following the naming convention
"""

import pandas as pd
from pathlib import Path
import re

# Define the scheme with named groups
pattern = re.compile(r'(?P<project>[a-zA-Z]*)(?P<date>[0-9]{2}[o-z][1-9A-V])(?P<step>[a-z]*)_')


# Function to group files by common project and date
def build_context(directory='.'):
    context = dict()

    # Iterate over files and directories in the specified folder
    for path in Path(directory).iterdir():
        if path.is_file():
            match = pattern.match(path.name)
            if match:
                project = match.group('project')
                date = match.group('date')
                step = match.group('step')
                if not project in context:
                    context[project] = dict()
                if not (date, step) in context[project]:
                    context[project][(date, step)] = list()
                context[project][(date, step)].append(path)
    return context

if __name__ == "__main__":
    context = build_context(Path.cwd())
    summary = pd.Series({project: len(context[project])
                         for project in context}).sort_values(ascending=False)
    print(summary)
