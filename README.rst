
=========
contexere
=========

Naming convention for research artefacts
----------------------------------------

Scientists and engineers create a multitude of digital artefacts during their daily work:
    - experimental results,
    - simulation results,
    - literate programming notebooks analysing experiments and simulations
    - statistical models,
    - machine learning models,
    - figures,
    - tables, etc

In order to trace and track these multiple interconnected research artefacts, hierarchical naming schemes
are a powerful tool to document the connection between research artefacts, find previous research outputs, and enable reproducible research [1].

The following naming scheme has evolved over several years to track research artefacts of all kinds:

The general scheme is: ``PIyymd[hMM]e[_x]__title``

-   ``PI``: [a-zA-Z]{2,} is the project identifier, which consists of at least two letters.
-   ``yy``: [0-9][0-9] are the last two digits of the years in the 21st century. I won't live beyond that. So, I do not care for following centuries.
-   ``m``: [o-z] these letters map to the respective months.
-   ``d``: [1-9,A-V] represent the 31 days of a month. Digits and upper-case characters have approximately the same height, such that this element gives a visual structure to the name, which divides the date from the daily counter.
-   ``h``: [a-x] these optional letters refer to the hours of the day
-   ``MM``: [0-5][0-9] are the minutes with 00 encoding the full hour
-   ``e``: [a-z]+ daily counter as lower-case letter enumerating the respective database or dataset. The 28th dataset would start with be enumerated as `aa`.
-   ``x``: Optional attribute being the last significant characters of the dataset, from which `DSyymde` is derived.
-   ``title``: Readable name of the respective data set with whitespaces being replaced by underscores.

+-------+-----------+-------+-----+-------+-----+-------+-----+
| month ``m``       | day ``d``   | day ``d``   | day ``d``   |
+=======+===========+=======+=====+=======+=====+=======+=====+
| ``o`` | January   | ``1`` |   1 | ``B`` |  11 | ``L`` |  21 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``p`` | February  | ``2`` |   2 | ``C`` |  12 | ``M`` |  22 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``q`` | March     | ``3`` |   3 | ``D`` |  13 | ``N`` |  23 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``r`` | April     | ``4`` |   4 | ``E`` |  14 | ``O`` |  24 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``s`` | May       | ``5`` |   5 | ``F`` |  15 | ``P`` |  25 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``t`` | June      | ``6`` |   6 | ``G`` |  16 | ``Q`` |  26 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``u`` | July      | ``7`` |   7 | ``H`` |  17 | ``R`` |  27 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``v`` | August    | ``8`` |   8 | ``I`` |  18 | ``S`` |  28 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``w`` | September | ``9`` |   9 | ``J`` |  19 | ``T`` |  29 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``x`` | October   | ``A`` |  10 | ``K`` |  20 | ``U`` |  30 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``y`` | November  |       |     |       |     | ``V`` |  31 |
+-------+-----------+-------+-----+-------+-----+-------+-----+
| ``z`` | December  |       |     |       |     |       |     |
+-------+-----------+-------+-----+-------+-----+-------+-----+

- The first dataset created on Friday 01.01.2021 would be named `DS21o1a`.
- The second dataset created on the same day would be named `DS21o1b`.
- An analysis (e.g. Jupyter notebook) of the first data set started after the second data set had been created would be named `DS21o1c_a`. Exported figures of this analysis should be named `DS21o1c_a__[plottype].[filetype]`.
- An analysis of data set `DS21o1b` started on 2nd January should be named `DS21o2a_1b`.
- An meta analysis of `DS21o1c_a` and `DS21o2a_1b` started on 11th February should be named `DS21pBa_o1c_2a`.

Installation
============
The module ``contexere`` can be installed from PyPi::

    pip install contexere

Usage
=====
The project provides the command line tool ``nxt``::

    usage: nxt [-h] [--version] [-g GROUP] [-k KEYWORDS [KEYWORDS ...]] [-l] [-p] [-r [REFERENCE]] [-s] [-u] [-v] [-vv] [target]

    Suggest name for research artefact

    positional arguments:
      target                Either a project identifier, filename, or folder

    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -g, --group GROUP     Project identifier for which the next research artefact GROUP will be suggested
      -k, --keywords KEYWORDS [KEYWORDS ...]
                            Optional argument for --clone adding one or more keywords to the filename
      -l, --local           Inspect files in current working dir only
      -p, --project         Create new project directory structure
      -r, --reference [REFERENCE]
                            Optional argument indicating reference of cloned file if used without arguments or accepting comma
                            separated list of references.
      -s, --summary         Summarise files following the naming convention
      -u, --utc             Generate timestamp with respect to UTC (default is local timezone)
      -v, --verbose         set loglevel to INFO
      -vv, --very-verbose   set loglevel to DEBUG

Calling the tool without any arguments returns the date abbreviation of today appended by the first daily counter (``a``)::

    nxt
    25s7a


    
References
==========

[1] Martin Kühne and Andreas W. Liehr. Improving the traditional information management in natural sciences. Data Science Journal, 8(1):18–26, 2009. doi: 10.2481/dsj.8.18.
