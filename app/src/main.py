import logging
import uvicorn

from fastapi import FastAPI
from fastapi.responses import Response, PlainTextResponse
import pandas as pd

from drive import service
from config import config
from charts import *
from processing import get_folder_table, search_file, monthly_cumulative_expenses
from db.connector import pg_engine
from config.variables import AccGroup


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

expense_folder = config.folders['expensemanager']


app = FastAPI()


@app.get("/")
def root():
    return {"message": "to be or not to be"}


@app.get("/files")
def get_files_dict() -> dict:

    results = service.files().list(q=f"'{expense_folder}' in parents",
                                   # pageSize=10,
                                   fields="nextPageToken, "
                                          "files(id, name, modifiedTime)"
                                   ).execute()
    items = results.get('files', [])

    files_table = pd.DataFrame(items)

    if 'modifiedTime' in files_table.columns:
        files_table['modifiedTime'] = pd.to_datetime(files_table['modifiedTime'])

    return files_table.to_dict()


@app.get("/test")
def test():
    # dump_schema(config.schema, pg_engine, dump_path=directories.root/'dump.sql')
    # dump_db(pg_engine, config.schema)
    # response = dump_db()

    return PlainTextResponse('Test')


@app.get("/chart")
async def chart(offset: int = 0):

    data = monthly_cumulative_expenses(file=testfile, accs=AccGroup.AED,
                                                 month_offset=offset)

    fig = plot_mom(data)

    # Return the PNG image as HTML
    png_output = yield_plot(fig)
    return Response(content=png_output.getvalue(), media_type="image/png")


@app.get("/update")
async def update_table():
    """Updates postgres table from downloaded csv file and dumps DB to hard drive"""
    df_folder = get_folder_table(expense_folder)

    for table in config.files:
        file = search_file(df_folder, table['file'])
        file.data.to_sql(name=table['table'], con=pg_engine, schema=config.schema, if_exists='replace')


    return PlainTextResponse(f"DB updated with file {file.name}")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
