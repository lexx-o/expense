from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

from config.variables import Columns, AccGroup
from dbio import Table
from processing import prepare_monthly_cumulative_expenses


dash_cumul = Dash(__name__, requests_pathname_prefix="/dash/chart/")


master = Table(name='master', schema='public')
df_raw = master.read(columns=[Columns.DATE, Columns.ACC, Columns.CAT, Columns.AMOUNT])
df_raw = df_raw[df_raw[Columns.ACC].isin(AccGroup.AED)]
df_raw = df_raw[~df_raw[Columns.CAT].isin(['Income', 'Account Transfer'])]

data = prepare_monthly_cumulative_expenses(df_expense=df_raw)

periods = data['period'].drop_duplicates().sort_index().values
marks_dict = {key: period for key, period in enumerate(periods)}


dropdown = dcc.Dropdown(
    id='dropdown',
    options=data['period'].drop_duplicates().sort_values().values,
    value=0,
)


slider = dcc.Slider(
    id='slider',
    value=max(marks_dict.keys()),
    marks=marks_dict,
    step=None,
    included=False,
)


dash_cumul.layout = html.Div(
    children=[
        dcc.Graph(id='cumul-chart'),
        slider,
    ]
)


@dash_cumul.callback(
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
        minreducedwidth=500,
        minreducedheight=500,
        hovermode='x',
        xaxis_range=(1, 31),
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        xaxis_zeroline=True,
        xaxis_zerolinewidth=2,
        xaxis_linecolor='black',
        xaxis_showgrid=False,
        xaxis_showspikes=True,
        xaxis_spikethickness=2,
        yaxis_dtick=10000,
        margin=dict(
            l=20,
            r=20,
            b=50,
            t=50,
            pad=4
        )

    )

    fig.add_trace(go.Scatter(
        x=df_slice.loc[df_slice['period'] == 'current', Columns.DAY],
        y=df_slice.loc[df_slice['period'] == 'current', 'runtot'],
        name='current',
        mode='lines+markers',
        line=dict(color='firebrick', width=3),
        hovertemplate=
            # 'Day %{x}<br>' +
            '<b>%{y:.0f}</b>'
    ))
    fig.add_trace(go.Scatter(
        x=df_slice.loc[df_slice['period'] == 'previous', Columns.DAY],
        y=df_slice.loc[df_slice['period'] == 'previous', 'runtot'],
        name='previous',
        mode='lines',
        line=dict(color='grey', width=2, dash='dot'),
        hovertemplate=
            # 'Day %{x}<br>' +
            '%{y:.0f}'
    ))

    return fig
