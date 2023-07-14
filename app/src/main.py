import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.wsgi import WSGIMiddleware

from config import config, directories
from config.variables import AccGroup
from charts import *
from processing import prepare_monthly_cumulative_expenses
from driveio import get_file, get_folder_table, get_files_dict
from dbio import Table, update_account_data_in_table
from db.connector import pg_engine


from dash_monthly_expense import dash_monthly_expense_app
from dash_balance import dash_balance_app
from dash_callbacks import dash_app


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

expense_folder = config.folders.expensemanager
master = Table(name='master', schema='public')


app = FastAPI()

templates = Jinja2Templates(directory=directories.templates)
app.mount('/static', StaticFiles(directory="static"), name="static")

app.mount("/dash/example/", WSGIMiddleware(dash_app.server))
app.mount("/dash/monthly_expense/", WSGIMiddleware(dash_monthly_expense_app.server))
app.mount("/dash/balance/", WSGIMiddleware(dash_balance_app.server))


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "home"})


@app.get("/files")
def get_files_dict_endpoint() -> dict:
    return get_files_dict(expense_folder)


@app.get("/chart", response_class=HTMLResponse)
async def chart(request: Request):
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "dash_monthly_expense",
                                                    })


@app.get("/chart2", response_class=HTMLResponse)
async def chart(request: Request):
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "dash_balance",
                                                    })


# @app.get("/chart_old", response_class=HTMLResponse)
# async def chart_old(request: Request, offset: int = 0):
#     table = master.read(engine=pg_engine, columns=[Columns.DATE, Columns.ACC, Columns.CAT, Columns.AMOUNT])
#     table = table[table[Columns.ACC].isin(AccGroup.AED)]
#     table = table[~table[Columns.CAT].isin(['Income', 'Account Transfer'])]
#
#     data = prepare_monthly_cumulative_expenses(df_expense=table)
#     fig = plot_monthly_cumulative_expenses(data, offset=offset)
#
#     img_string = yield_plot(fig)
#
#     return templates.TemplateResponse("page.html", {"request": request,
#                                                     "pagename": "chart",
#                                                     "img_data": img_string})


@app.get("/dash", response_class=HTMLResponse)
async def chart(request: Request):
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "dash",
                                                    })



@app.get("/file_upload", response_class=HTMLResponse)
async def upload_new_data(request: Request, id: str):
    """
    Updates postgres tables from downloaded csv file.
    Checks for account names present in the file and updates entries in the database for these accounts only.
    """
    folder = get_folder_table(expense_folder)
    file = get_file(folder, id=id)
    df = file.data

    update_account_data_in_table(data=df, table=master, engine=pg_engine)
    msg = f"DB update process finished. Table entries added/updated: {df.shape[0]}"

    # return PlainTextResponse(f"DB update process finished. Table entries added/updated: {df.shape[0]}")
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "db_updated",
                                                    "message": msg,
                                                    "folder": folder})


@app.get("/update", response_class=HTMLResponse)
async def template_upload(request: Request):

    folder = get_folder_table(expense_folder)

    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "update_form",
                                                    "folder": folder})


# @app.get("/test")
# def test():
#     return 'Test'


# @app.get("/dash")
# def dash_chart():
#     out = dash_barchart(dash_app)


logger.info('STARTING SERVER')


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)