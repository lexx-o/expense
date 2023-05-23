import logging
import uvicorn

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import Response, PlainTextResponse

from config import config
from config.variables import AccGroup
from charts import *
from processing import monthly_cumulative_expenses
from driveio import get_file, get_folder_table, get_files_dict
from db.connector import pg_engine


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

expense_folder = config.folders['expensemanager']


app = FastAPI()


@app.get("/")
def root():
    return {"message": "to be or not to be"}


@app.get("/files")
def get_files_dict_endpoint() -> dict:
    return get_files_dict(expense_folder)


# @app.get("/test")
# def test():
#     # dump_schema(config.schema, pg_engine, dump_path=directories.root/'dump.sql')
#     # dump_db(pg_engine, config.schema)
#     # response = dump_db()
#
#     return PlainTextResponse('Test')


@app.get("/chart")
async def chart(offset: int = 0):
    table = pd.read_sql(sql=f"SELECT * FROM {config.schema}.current",
                        con=pg_engine)

    data = monthly_cumulative_expenses(data=table,
                                       accs=AccGroup.AED,
                                       month_offset=offset)

    fig = plot_mom(data)

    # Return the PNG image as HTML
    png_output = yield_plot(fig)
    return Response(content=png_output.getvalue(), media_type="image/png")


@app.get("/update")
async def update_table():
    """Updates postgres table from downloaded csv file and dumps DB to hard drive"""
    df_folder = get_folder_table(expense_folder)

    for part in config.partitions:
        partition = config.partitions[part]
        filename = partition['file']
        tablename = partition['table']

        file = get_file(df_folder, filename)
        file.data.to_sql(name=tablename, con=pg_engine, schema=config.schema, if_exists='replace')

    return PlainTextResponse(f"DB updated")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
