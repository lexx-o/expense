from config import config, directories

from config.variables import AccGroup, Columns

from dbio import Table, update_account_data_in_table
from db.connector import pg_external
from charts import *
import pandas as pd
from datetime import date

from dash import Dash, callback, Output, Input
import plotly.express as px
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse
import uvicorn

from dash_dummy import dash_dummy


# @app.get("/dash", response_class=HTMLResponse)
# async def chart():
#     # return templates.TemplateResponse("page.html", {"request": request,
#     #                                                 "pagename": "chart",
#     #                                                 # "img_data": img_string
#     #                                                 })
#     return dash_dummy



# def main():
#     table = Table(name='master', schema='public')
#     df_raw = table.read(columns=[Columns.DATE, Columns.ACC, Columns.CAT, Columns.AMOUNT], engine=pg_external)
#     df_raw = df_raw[df_raw[Columns.ACC].isin(AccGroup.AED)]
#     df_raw = df_raw[~df_raw[Columns.CAT].isin(['Income', 'Account Transfer'])]
#
#     df_expenses_daily = df_raw.groupby(by=Columns.DATE).sum()[[Columns.AMOUNT]]
#     date_range = pd.date_range(df_expenses_daily.index.min(), df_expenses_daily.index.max())
#     df_expenses_daily = df_expenses_daily.reindex(date_range, fill_value=0)
#
#     df_expenses_daily[Columns.AMOUNT] *= -1
#     df_expenses_daily[Columns.DAY] = df_expenses_daily.index.day
#
#     df_expenses_daily['_period_id'] = df_expenses_daily.index.month + df_expenses_daily.index.year * 12
#     df_expenses_daily['offset'] = df_expenses_daily['_period_id'] - (date.today().month + date.today().year * 12)
#     df_expenses_daily['runtot'] = df_expenses_daily[['offset', Columns.AMOUNT]].groupby('offset').cumsum()
#
#     df_expenses_daily['period'] = \
#         df_expenses_daily.index.year.astype(str) \
#         + "-" \
#         + df_expenses_daily.index.month.astype(str)
#
#     return df_expenses_daily



if __name__ == '__main__':

    dash_dummy.run(debug=True)
    # uvicorn.run("run_test:app", host="127.0.0.1", port=8008, reload=True)
    # main()