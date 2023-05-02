from io import BytesIO
import random

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def yield_plot(fig: Figure) -> BytesIO:

    # Render the figure as a PNG image
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)

    return png_output


def plot_mom(x1, x2):
    # Create a figure and plot the data
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xrange(1, 31)


    return fig

def random_data():
    # Create some random data for the chart
    x = [i for i in range(10)]
    y = [random.randint(1, 10) for i in range(10)]
    return x, y