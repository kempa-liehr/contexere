from loguru import logger
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()

def savefig(stem, ax=plt, suffix='pdf', path=FIGURES_DIR):
    fn = f'{stem}.{suffix}'
    ax.savefig(path / fn, bbox_inches='tight')
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
