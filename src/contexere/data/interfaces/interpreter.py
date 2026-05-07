import os
import sys

def get_execution_context():
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

        # --- Script execution: use __main__ module ---
    main_module = sys.modules.get("__main__")

    if main_module and hasattr(main_module, "__file__"):
        return "script", os.path.basename(main_module.__file__)

    # Fallback (interactive / embedded)
    return "script", None

if __name__ == "__main__":
    context, name = get_execution_context()
    if context == "notebook":
        print(f"Running in notebook: {name}")
    else:
        print(f"Running as script: {name}")