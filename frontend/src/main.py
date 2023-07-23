import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.wsgi import WSGIMiddleware

from config import directories
from dash_monthly_expense import dash_monthly_expense_app
from dash_balance import dash_balance_app

from util import df_from_endpoint, data_from_endpoint

app = FastAPI()
templates = Jinja2Templates(directory=directories.templates)
app.mount('/static', StaticFiles(directory="static"), name="static")
app.mount("/dash/monthly_expense/", WSGIMiddleware(dash_monthly_expense_app.server))
app.mount("/dash/balance/", WSGIMiddleware(dash_balance_app.server))


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    """Main landing page"""
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "home"})


@app.get("/monthly_exp", response_class=HTMLResponse)
async def chart(request: Request):
    """Monthly expense chart page. Shows expense accrual vs previous month for any selected month"""
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "dash_monthly_expense",
                                                    })


@app.get("/balance", response_class=HTMLResponse)
async def chart(request: Request):
    """ Page showing overall balance by accounts over days"""
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "dash_balance",
                                                    })


@app.get("/update", response_class=HTMLResponse)
async def template_upload(request: Request):
    """Page which allows select specific file from expense_manager folder and update the DB with its data"""
    folder = df_from_endpoint("http://backend:8000/file-list")

    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "update_form",
                                                    "folder": folder,
                                                    })


@app.get("/file_upload", response_class=HTMLResponse)
async def upload_new_data(request: Request, id: str):
    """
    Updates postgres tables from downloaded csv file.
    Checks for account names present in the file and updates entries in the database for these accounts only.
    """
    result = data_from_endpoint(f"http://backend:8000/update-db-with-file?id={id}")
    msg = f"DB update process finished. Table entries added/updated: {result['shape'][0]}"
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "db_updated",
                                                    "message": msg,
                                                    })


@app.get("/test")
async def test():
    resp = requests.get("http://drive-reader:8000/test")
    return resp.content.decode('utf-8')


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
