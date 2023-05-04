from io import BytesIO
import random

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib import pyplot as plt

from config.variables import Columns

def yield_plot(fig: Figure) -> BytesIO:

    # Render the figure as a PNG image
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)

    return png_output


def plot_mom(df):
    # Create a figure and plot the data
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(1, 31)

    current = df.loc[df['period'] == 'current', ['day', 'runtot']]
    ax.plot(current['day'], current['runtot'], c='r', lw=2, label='current')

    previous = df.loc[df['period'] == 'previous', ['day', 'runtot']]
    ax.plot(previous['day'], previous['runtot'], c='grey', lw=1, ls=':', label='previous')

    year = df.loc[df['period'] == 'current', Columns.DATE].dt.year.unique()[0]
    month = df.loc[df['period'] == 'current', Columns.DATE].dt.month.unique()[0]
    fig.suptitle(f'Cumulative spend over {year}-{month}')
    ax.legend()

    # plt.show()

    return fig

def random_data():
    # Create some random data for the chart
    x = [i for i in range(10)]
    y = [random.randint(1, 10) for i in range(10)]
    return x, y