
======
pyName
======


    Naming convention for data artefacts

The general scheme is: `DSyymd[hMM]e[_x]__title`

-   **`DS`:** Initials of project. `DS` is the abbreviation of *Data Science*
-   **`yy`:** [0-9][0-9] are the last two digits of the years in the 21st century. I won't live beyond that. So, I do not care for following centuries. This is conform to the 2018 scheme and the schemes before 2000.
-   **`m`:** [o-z] these letters map to the respective months.
-   **`d`:** [1-9,A-V] represent the 31 days of a month. Digits and upper-case characters have approximately the same height, such that this element gives a visual structure to the name, which divides the date from the daily counter.
-   **`h`:** [a-x] these optional letters refer to the hours of the day
-   **`MM`:** [0-5][0-9] are the minutes with 00 encoding the full hour
-   **`e`:** [a-z]+ daily counter as lower-case letter enumerating the respective database or dataset. The 28th dataset would start with be enumerated as `aa`.
-   **`x`:** Optional attribute being the last significant characters of the dataset, from which `DSyymde` is derived.
-   **`title`:** Readable name of the respective data set with whitespaces being replaced by underscores.

|-----+-----------+-----+-----+-----+-----+-----+-----+------+-----+------+-----|
| `m` | month     | `d` | day | `d` | day | `d` | day | hour | `h` | hour | `h` |
|=====+===========+=====+=====+=====+=====+=====+=====+======+=====+======+=====|
| `o` | January   | `1` |   1 | `B` |  11 | `L` |  21 |    0 | a   |   12 | m   |
| `p` | February  | `2` |   2 | `C` |  12 | `M` |  22 |    1 | b   |   13 | n   |
| `q` | March     | `3` |   3 | `D` |  13 | `N` |  23 |    2 | c   |   14 | o   |
| `r` | April     | `4` |   4 | `E` |  14 | `O` |  24 |    3 | d   |   15 | p   |
| `s` | May       | `5` |   5 | `F` |  15 | `P` |  25 |    4 | e   |   16 | q   |
| `t` | June      | `6` |   6 | `G` |  16 | `Q` |  26 |    5 | f   |   17 | r   |
| `u` | July      | `7` |   7 | `H` |  17 | `R` |  27 |    6 | g   |   18 | s   |
| `v` | August    | `8` |   8 | `I` |  18 | `S` |  28 |    7 | h   |   19 | t   |
| `w` | September | `9` |   9 | `J` |  19 | `T` |  29 |    8 | i   |   20 | u   |
| `x` | October   | `A` |  10 | `K` |  20 | `U` |  30 |    9 | j   |   21 | v   |
| `y` | November  |     |     |     |     | `V` |  31 |   10 | k   |   22 | w   |
| `z` | December  |     |     |     |     |     |     |   11 | l   |   23 | x   
|-----+-----------+-----+-----+-----+-----+-----+-----+------+-----+------+-----|


The first dataset created on <span class="timestamp-wrapper"><span class="timestamp">[2021-01-01 Fri] </span></span> would be named `DS21o1a`.


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
