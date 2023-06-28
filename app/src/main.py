import logging
import uvicorn

from fastapi import FastAPI
from fastapi.responses import Response, PlainTextResponse

from config import config
from config.variables import AccGroup
from charts import *
from processing import monthly_cumulative_expenses
from driveio import get_file, get_folder_table, get_files_dict
from dbio import Table, update_account_data_in_table
from db.connector import pg_engine


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

expense_folder = config.folders['expensemanager']
master = Table(name='master', schema='public')


app = FastAPI()


@app.get("/")
def root():
    return {"message": "to be or not to be"}


@app.get("/files")
def get_files_dict_endpoint() -> dict:
    return get_files_dict(expense_folder)


@app.get("/chart")
async def chart(offset: int = 0):
    table = master.read(engine=pg_engine)

    data = monthly_cumulative_expenses(data=table,
                                       accs=AccGroup.AED,
                                       month_offset=offset)

    fig = plot_mom(data)

    # Return the PNG image as HTML
    png_output = yield_plot(fig)
    return Response(content=png_output.getvalue(), media_type="image/png")


@app.get("/test")
def test():
    return 'Test'


@app.get("/update")
async def upload_new_data(file: str):
    """
    Updates postgres tables from downloaded csv file.
    Checks for account names present in the file and updates entries in the database for these accounts only.
    """
    df_folder = get_folder_table(expense_folder)
    file = get_file(df_folder, file)
    df = file.data

    update_account_data_in_table(data=df, table=master, engine=pg_engine)

    return PlainTextResponse(f"DB update process finished. Table entries added/updated: {df.shape[0]}")


if __name__ == '__main__':
    logger.info('STARTING SERVER')
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
