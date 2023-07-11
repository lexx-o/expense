import base64
import random
from io import BytesIO

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from config.variables import Columns


def yield_plot(fig: Figure) -> str:
    """
    Transforms a Figure object into base64 encoded string
    Args:
        fig: a Figure object
    Returns: str bytes64 string
    """
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)

    b64_stream = base64.b64encode(png_output.getvalue()).decode("utf-8")

    return b64_stream


def plot_monthly_cumulative_expenses(data: pd.DataFrame, offset: int = 0) -> plt.Figure:

    df_slice = data[(data['offset'] - offset).isin([-1, 0])]

    curr_period = df_slice.loc[df_slice['offset'] == df_slice['offset'].max()]
    prev_period = df_slice.loc[df_slice['offset'] < df_slice['offset'].max()]

    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(1, 31)

    ax.plot(curr_period[Columns.DAY], curr_period['runtot'], c='r', lw=2, label='current')
    ax.plot(prev_period[Columns.DAY], prev_period['runtot'], c='grey', lw=1, ls=':', label='previous')

    year = curr_period.index.year.unique()[0]
    month = curr_period.index.month.unique()[0]
    fig.suptitle(f'Cumulative spend over {year}-{month}')
    ax.legend()

    return fig


def random_data():
    # Create some random data for the chart
    x = [i for i in range(10)]
    y = [random.randint(1, 10) for i in range(10)]
    return x, y
