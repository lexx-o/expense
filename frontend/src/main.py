import pandas as pd
import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from config import config, directories
from util import request_from_endpoint


app = FastAPI()
templates = Jinja2Templates(directory=directories.templates)
app.mount('/static', StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    """Main landing page"""
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "home"})


@app.get("/monthly_exp", response_class=HTMLResponse)
async def chart(request: Request):
    """Monthly expense chart page. Shows expense accrual vs previous month for any selected month"""
    dash_url = f"http://{config.app.dash.name}:{config.app.dash.port}/monthly_expense"
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "dash_monthly_expense",
                                                    "dash_url": dash_url
                                                    })


@app.get("/balance", response_class=HTMLResponse)
async def chart(request: Request):
    """ Page showing overall balance by accounts over days"""
    dash_url = f"http://{config.app.dash.name}:{config.app.dash.port}/balance"
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "dash_balance",
                                                    "dash_url": dash_url
                                                    })


@app.get("/update", response_class=HTMLResponse)
async def template_upload(request: Request):
    """
    Page which allows select specific file from expense_manager folder and update the DB with its data
    """
    url = f"http://{config.app.backend.name}:{config.app.backend.port}/file-list"
    resp = request_from_endpoint(url)
    if resp['status'] == 0:
        folder = pd.DataFrame(resp['data'])
    else:
        folder = None

    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "update_form",
                                                    "status": resp['status'],
                                                    "folder": folder
                                                    })


@app.get("/file_upload", response_class=HTMLResponse)
async def upload_new_data(request: Request, id: str):
    """
    Updates postgres tables from downloaded csv file.
    Checks for account names present in the file and updates entries in the database for these accounts only.
    """
    url = f"http://{config.app.backend.name}:{config.app.backend.port}/update-db-with-file?id={id}"
    resp = request_from_endpoint(url)
    if resp['status'] == 0:
        msg = f"DB update process finished. Table entries added/updated: {resp['data']['shape'][0]}"
    else:
        msg = resp['data']
    return templates.TemplateResponse("page.html", {"request": request,
                                                    "pagename": "db_updated",
                                                    "status": resp['status'],
                                                    "message": msg,
                                                    })


@app.get("/test")
async def test():
    resp = requests.get(f"http://{config.app.dash.name}:8000/")
    return resp.content.decode('utf-8')


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
