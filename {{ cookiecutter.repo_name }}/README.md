# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Project Organization

```
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
{% if cookiecutter.dependency_file == 'environment.yml' %}├── environment.yml    <- Configuration file for Conda environments
│                         https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html{% endif %}
{% if cookiecutter.open_source_license != 'No license file' %}├── LICENSE            <- Open-source license{% endif %}
├── Makefile           <- Makefile with convenience commands like `make create_environment`
│
├── notebooks          <- Jupyter notebooks. Naming convention follows `contexere` syntax:
│   │                     {{ cookiecutter.repo_name }}yymDc[_link[_link]]__keyword.ipynb with
│   │                     `yy` is the two-digit truncated year
│   │                     `m` is the abbreviated month
│   │                     `D` is the abbreviated year
│   │                     `c` is the research artefact group counter
│   │                     `link` is the abbreviated predecessor research artefact group identifier
│   │                     `keyword` is a list of underscore-separated keywords
│   └── 00_{{ cookiecutter.module_name }}_template.ipynb   <- Template Jupyter notebook
│
├── pyproject.toml     <- Project configuration file with package metadata for
│                         {{ cookiecutter.module_name }} and configuration for tools like black
├── README.md          <- The top-level README for researchers using this project.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│   └── {{ cookiecutter.module_name }}_bibliography.bib    <- Template bibliography
│
├── reports            <- Generated analysis like presentations and manuscripts directed to audiences outside the core research team
│
{% if cookiecutter.include_code_scaffold == 'Yes' %}├── results
│   ├── {{ cookiecutter.repo_name }}_logbook.org   <- Template for documenting experiments, analysis, insights, and ideas
│   └── figs           <- Generated graphics and figures to be used in reporting and results documentation
│
├── src
│   └── {{ cookiecutter.module_name }}   <- Source code for use in this project.
│       │
│       ├── __init__.py             <- Makes {{ cookiecutter.module_name }} a Python module
│       │
│       ├── config.py               <- Store useful variables and configuration
│       │
│       ├── dataset.py              <- Scripts to download or generate data
│       │
│       ├── features.py             <- Code to create features for modeling
│       │
│       ├── modeling
│       │   ├── __init__.py
│       │   ├── predict.py          <- Code to run model inference with trained models
│       │   └── train.py            <- Code to train models
│       │
│       └── plots.py                <- Code to create visualizations
│
└── tests             <- Unit testing templates
{% else %}└── results
    ├── {{ cookiecutter.repo_name }}_logbook.org   <- Template for documenting experiments, analysis, insights, and ideas
    └── figs           <- Generated graphics and figures to be used in reporting and results documentation
{% endif %}
```

--------

