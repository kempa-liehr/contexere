from __future__ import annotations

import os
from typing import Tuple


def get_execution_context() -> Tuple[str, str | None]:
    """
    Determine whether the code is running in a Python script or a Jupyter notebook.

    Returns
    -------
    (context, name)
        context : str
            Either 'notebook' or 'script'
        name : str | None
            Notebook name (without .ipynb) or script filename,
            or None if it cannot be determined.
    """
    # --- Try to detect Jupyter ---
    try:
        from IPython import get_ipython

        ip = get_ipython()
        if ip is not None:
            shell = ip.__class__.__name__

            if shell in ("ZMQInteractiveShell",):
                # Running inside Jupyter
                try:
                    import ipynbname
                    return "notebook", ipynbname.name()
                except Exception:
                    return "notebook", None

            elif shell in ("TerminalInteractiveShell",):
                # IPython terminal, treat as script-like
                pass

    except Exception:
        pass

    # --- Fallback: assume script execution ---
    try:
        return "script", os.path.basename(__file__)
    except NameError:
        # Interactive Python shell or edge case
        return "script", None