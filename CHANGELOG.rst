=========
Changelog
=========

Version 1.2.0
=============
- Define convenience plotting functions `distribution()` and `distributions()` if the respective packages are available.
- Extend dependencies such that the template Python package can be imported in a standard data science environment.
- Ensure that the project template is included in the Python package.
- Fix missing RAG in files created with `savefig()`.
- Figure metadata reference the suffix of the creating script.
- Fix `graphicspath` in LaTeX template.
- Fix SVG metadata.


Version 1.1.0
=============
- Add cloning of research artefacts
- Add `savefig()` function to the source code scaffold supporting , which supports saving of metadata.
- Add template LaTeX report
- Add template Jupyter notebook
- Add `results` folder and remove `models` folder
- Cloned research artefacts are automatically added to the local git repository

Version 1.0.0
=============
- Rename CLI from `name` to `nxt` (pronounce "next")
- Provide command line argument for summarising the research artefact groups in a directory tree
- Build SQLite database of linked research artefacts
- Add command line argument for initialising project directory structure and code scaffold.

Version 0.5.0
=============
- Fix regular expression make trailing underscore optional
- Except directories as artefacts
- CLI assumes local time zone as default

Version 0.4.1
=============
- Get timestamp indicating start of next month
- Add option to abbreviate timestamps with respect to local time instead of UTC

