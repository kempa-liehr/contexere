from contexere.data.interfaces.interpreter import get_execution_context
from loguru import logger
from pathlib import Path
from tqdm import tqdm
import typer

engineering_colors = ['#00467F', '#009AC7', '#8D9091', '#A71930', '#7D0063', '#D2492A', '#55A51C', '#4F2D7F',
                      '#005B82', '#00877C', '#0039A6']
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    sns.set_palette(engineering_colors)

    def distribution(series, log_transformed=False,
                     swarmplot=False,
                     bins='auto'):
        '''
        Visualize distribution of pandas.Series as combination of histogram and boxplot

        The code has been adapted from ENGSCI762 Data Science module

        :param series: pandas.Series
        :return: fig
        '''
        # http://stackoverflow.com/questions/40070093/gridspec-on-seaborn-subplots
        gridkw = dict(height_ratios=[5, 1])
        fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw=gridkw, sharex=True)
        if log_transformed:
            feature = pd.Series(np.log(series),
                                name='log({})'.format(series.name)
                                )
        else:
            feature = series
        sns.histplot(x=feature, ax=ax1, kde=False, bins=bins)  # array, top subplot
        sns.boxplot(x=feature, ax=ax2, width=.4)  # bottom subplot
        if swarmplot:
            sns.swarmplot(feature, ax=ax2,
                          size=2, color=".3", linewidth=0)

        ax1.set_xlabel('')
        ax1.text(1.05, 0.95,
                 feature.describe().to_string(),
                 transform=ax1.transAxes, fontsize=14,
                 verticalalignment='top')
        # http://stackoverflow.com/questions/29813694/how-to-add-a-title-to-seaborn-facet-plot
        fig.subplots_adjust(top=0.9)
        fig.suptitle(feature.name, fontsize=16)
        return fig, (ax1, ax2)


    def distributions(series, species, log_transformed=False,
                      both_series=False, bins='auto',
                      colors=[engineering_colors[1],
                              engineering_colors[3]]):
        '''
        Visualize distribution of pandas.Series as combination of histogram and boxplot

        The code has been adapted from ENGSCI762 Data Science module

        :param series: pandas.Series
        :return: fig
        '''
        # http://stackoverflow.com/questions/40070093/gridspec-on-seaborn-subplots
        gridkw = dict(height_ratios=[5, 1, 1])
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw=gridkw, sharex=True)

        labels = np.unique(species)
        if log_transformed:
            feature = pd.Series(np.log(series),
                                name='log({})'.format(series.name)
                                )
        else:
            feature = series
        if not both_series:
            A = feature[species == labels[0]]
            B = feature[species == labels[1]]
            Alabel = labels[0]
            Blabel = labels[1]
        else:
            A = feature
            B = species
            Alabel = feature.name
            Blabel = species.name

        sns.histplot(x=A, ax=ax1,
                     kde=False,
                     label=Alabel,
                     color=colors[0],
                     bins=bins
                     )  # array, top subplot
        sns.histplot(x=B, ax=ax1,
                     kde=False,
                     label=Blabel,
                     color=colors[1],
                     bins=bins)  # array, top subplot
        ax1.legend()
        ax1.set_xlabel('')
        sns.boxplot(x=A, ax=ax2, width=.4,
                    color=colors[0])  # middle subplot
        ax2.set_xlabel('')

        current_palette = colors
        sns.boxplot(x=B, ax=ax3, width=.4,
                    color=colors[1]
                    )  # bottom subplot
        return fig, (ax1, ax2, ax3)

except ImportError:
    plt = None

from {{ cookiecutter.module_name }}.config import FIGURES_DIR, PROCESSED_DATA_DIR, AUTHOR_NAME, PROJECT_NAME, PROJECT_ID

app = typer.Typer()

def savefig(stem, plotter=plt, suffix='pdf', path=FIGURES_DIR,
            author=AUTHOR_NAME, project_id=PROJECT_ID, project_name=PROJECT_NAME):
    script_suffix, script_name = get_execution_context()
    rag = script_name.split('__')[0]
    implicit_suffix = stem.split('.')[-1]
    if implicit_suffix in ['pdf', 'png', 'svg']:
        fn = f"{rag}__{stem.replace(' ', '_')}"
    else:
        assert suffix in ['pdf', 'png', 'svg']
        fn = f"{rag}__{stem.replace(' ', '_')}.{suffix}"
        implicit_suffix = suffix
    filepath = path / fn
    
    descriptor = {'Contributor' if implicit_suffix == 'svg' else 'Author': author,
                  'Title': f'{stem} -- {project_name} ({project_id})',
                  'Creator': f'{script_name}.{script_suffix}',
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
