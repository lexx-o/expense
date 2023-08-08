import uvicorn
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware

from dash_monthly_expense import dash_monthly_expense_app
from dash_balance import dash_balance_app


app = FastAPI()
app.mount("/monthly_expense/", WSGIMiddleware(dash_monthly_expense_app.server))
app.mount("/balance/", WSGIMiddleware(dash_balance_app.server))


@app.get("/")
def root() -> dict:
    """No functionality implemented on root"""
    return {'name': 'dash',
            'status': 'healthy'}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
