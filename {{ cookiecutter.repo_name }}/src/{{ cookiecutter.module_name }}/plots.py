from contexere.data.interfaces.interpreter import get_execution_context
from loguru import logger
from pathlib import Path
from tqdm import tqdm
import typer

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

from {{ cookiecutter.module_name }}.config import FIGURES_DIR, PROCESSED_DATA_DIR, AUTHOR_NAME, PROJECT_NAME, PROJECT_ID

app = typer.Typer()

def savefig(stem, plotter=plt, suffix='pdf', path=FIGURES_DIR,
            author=AUTHOR_NAME, project_id=PROJECT_ID, project_name=PROJECT_NAME):
    implicit_suffix = stem.split('.')[-1]
    if implicit_suffix in ['pdf', 'png', 'svg']:
        fn = stem
    else:
        assert suffix in ['pdf', 'png', 'svg']
        fn = f'{stem}.{suffix}'
        implicit_suffix = suffix
    filepath = path / fn
    descriptor = {'Contributor' if implicit_suffix == 'svg' else 'Author': author,
                  'Title': f'{stem} -- {project_name} ({project_id})',
                  'Creator': get_execution_context()[1],
                  }
    if plotter is None:
        logger.warning(f'File {fn} cannot be saved, because `plotter` is {str(plotter)}!.')
    elif not hasattr(plotter, 'savefig'):
        logger.warning(f'File {fn} cannot be saved, because `plotter` {str(plotter)} does not implement `.savefig()`!')
    else:
        try:
            plotter.savefig(filepath, bbox_inches='tight', metadata=descriptor)
        except:
            logger.warning(
                f"File {fn} cannot be saved, because `plotter` {str(plotter)} does not implement options `bbox_inches` and `metadata` as defined by matplotlib.pyplot.savefig()!")
    return fn


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating plot from data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
