from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

from config.variables import Columns, AccGroup
from dbio import Table
from processing import prepare_monthly_cumulative_expenses


dash_monthly_expense_app = Dash(__name__, requests_pathname_prefix="/dash/monthly_expense/")


master = Table(name='master', schema='public')
data = prepare_monthly_cumulative_expenses(master)

periods = data['period'].drop_duplicates().sort_index().values
marks_dict = {key: period for key, period in enumerate(periods)}


slider = dcc.Slider(
    id='slider',
    value=max(marks_dict.keys()),
    marks=marks_dict,
    step=None,
    included=False,
)


dash_monthly_expense_app.layout = html.Div(
    children=[
        dcc.Graph(id='cumul-chart'),
        slider,
    ]
)


@dash_monthly_expense_app.callback(
    Output('cumul-chart', 'figure'),
    Input('slider', 'value')
)
def cumul_chart(slider_position):
    # slider only accepts positive marks
    offset_value = slider_position - max(marks_dict.keys())
    df_slice = data[(data['offset'] - offset_value).isin([-1, 0])]

    df_slice.loc[df_slice['offset'] == offset_value, 'period'] = 'current'
    df_slice.loc[df_slice['offset'] < offset_value, 'period'] = 'previous'

    fig = go.Figure()

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
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(210,210,210,0.8)',

        # ranges and panning
        xaxis_range=(0.5, 31.5),
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,

        # x-axis line
        yaxis_zeroline=True,
        yaxis_zerolinewidth=2,
        yaxis_zerolinecolor='grey',

        # gridlines
        xaxis_showgrid=False,
        xaxis_showspikes=True,
        xaxis_spikethickness=2,
        yaxis_dtick=5000,

        # legend
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    fig.add_trace(go.Scatter(
        x=df_slice.loc[df_slice['period'] == 'current', Columns.DAY],
        y=df_slice.loc[df_slice['period'] == 'current', 'runtot'],
        name='current month',
        mode='lines+markers',
        line=dict(color='firebrick', width=3),
        hovertemplate=
            # 'Day %{x}<br>' +
            '<b>%{y:.0f}</b>'
    ))
    fig.add_trace(go.Scatter(
        x=df_slice.loc[df_slice['period'] == 'previous', Columns.DAY],
        y=df_slice.loc[df_slice['period'] == 'previous', 'runtot'],
        name='previous month',
        mode='lines',
        line=dict(color='grey', width=2, dash='dot'),
        hovertemplate=
            # 'Day %{x}<br>' +
            '%{y:.0f}'
    ))
    fig.add_shape(type='line', x0=0.5, x1=31, y0=20000, y1=20000, line=dict(color='red', width=0.5))
    # fig.add_shape(type='rect', xref='paper', yref='paper', x0=0, x1=1, y0=0, y1=1, line=dict(color='black', width=1))


    return fig
