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
from dbio import read_table_update_log, write_table_update_log
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


@app.get("/test")
def test():
    return 'Test'


@app.get("/update")
async def update_tables():
    """Updates postgres tables from downloaded csv files"""
    log = read_table_update_log(pg_engine)
    modified = get_latest_log(log)

    df_folder = get_folder_table(expense_folder)

    updated_tables = []
    for part in config.partitions:
        file = get_file(df_folder, config.partitions[part]['file'])
        table_timestamp_db = modified.loc[part, 'modified']

        if file.modified <= table_timestamp_db:
            pass
        else:
            tablename = config.partitions[part]['table']
            file.data.to_sql(name=tablename,
                             con=pg_engine,
                             schema=config.schema,
                             if_exists='replace')
            write_table_update_log(partition=part, file=file, engine=pg_engine)
            updated_tables.append(tablename)

    return PlainTextResponse(f"DB update process finished. Tables updated with new data: {updated_tables}")


def get_latest_log(log: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(index=config.partitions.keys())
    latest = log.sort_values(by=['dttm'], ascending=False).groupby(by=['partition']).last()
    modified_times = df.join(latest)
    modified_times['modified'] = pd.to_datetime(modified_times['modified'])
    return modified_times


if __name__ == '__main__':
    logger.info('STARTING SERVER')
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
