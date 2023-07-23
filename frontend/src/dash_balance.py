import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

from config.variables import Columns
from util import df_from_endpoint


dash_balance_app = Dash(__name__, requests_pathname_prefix="/dash/balance/")


def _serve_layout():

    global data
    data = df_from_endpoint("http://backend:8000/balance-table")

    date_range = pd.date_range(start=data[Columns.DATE].min(), end=data[Columns.DATE].max())

    global date_range_df
    date_range_df = pd.DataFrame(date_range)

    marks_dict = {n: date.strftime('%Y-%m') for n, date in zip(date_range_df.index, date_range_df[0]) if date.day == 1}

    slider = dcc.RangeSlider(
        id='slider',
        min=date_range_df.index.min(),
        max=date_range_df.index.max(),

        value=[max(0, date_range_df.index.max() - 31), date_range_df.index.max()],
        marks=marks_dict,
        step=1,
        # tooltip={"placement": "bottom", "always_visible": True},
        # included=False,
    )

    return html.Div(
        children=[
            html.Div(id='textbox'),
            dcc.Graph(id='balance-chart'),
            slider,
        ]
    )


dash_balance_app.layout = _serve_layout


@dash_balance_app.callback(
    Output('balance-chart', 'figure'),
    # Output('textbox', 'children'),
    Input('slider', 'value')
)
def plot_balance_chart(selection):

    fig = go.Figure()

    date_min = date_range_df.loc[selection[0], 0]
    date_max = date_range_df.loc[selection[1], 0]

    mask = (data[Columns.DATE] >= date_min) & (data[Columns.DATE] <= date_max)

    df = data[mask]

    accs = df[Columns.ACC].unique()
    for i, acc in enumerate(accs):
        acc_df = df[df[Columns.ACC] == acc]
        fig.add_trace(go.Scatter(
            x=acc_df[Columns.DATE],
            y=acc_df['Balance'],
            name=acc,
            mode='lines',
            line=dict(width=1, shape='hvh'),
            fill='tozeroy' if i == 0 else 'tonexty',
            stackgroup='one',
            hovertemplate=
            # 'Day %{x}<br>' +
            '<b>%{y:,.2f}</b>'
        ))

    yrange_min = max(0, df.loc[df[Columns.ACC] == 'AED ENBD', 'Balance'].min() - 5000)
    yrange_max = df[df[Columns.ACC] != 'Credit ENBD'].groupby(by=Columns.DATE)['Balance'].sum().max() * 1.05

    fig.update_layout(
        height=600,
        margin=dict(
            l=20,
            r=20,
            b=20,
            t=20,
            pad=4
        ),
        hovermode='x',

        font=dict(
            size=14,
        ),
        paper_bgcolor='rgba(210,210,210,0.8)',
        plot_bgcolor='rgba(0,0,0,0)',
        # plot_bgcolor='rgba(195,195,195,0.5)',

        xaxis_showgrid=False,
        # xaxis_showspikes=True,
        # xaxis_spikethickness=1,
        # xaxis_zeroline=False,

        yaxis_range=[yrange_min, yrange_max],
        # yaxis_fixedrange=True,
        yaxis_zeroline=True,
        yaxis_zerolinewidth=2,
        yaxis_zerolinecolor='grey',


        # legend=dict(
        #     yanchor="top",
        #     xanchor="right",
        #     x=0.99
        #     y=0.99,
        # )
        )

    return fig
