import uvicorn
import psycopg2

from fastapi import FastAPI
from fastapi.responses import Response
import pandas as pd

from drive import service
from config import config, directories
from charts import *
from processing import get_folder_table, search_file, File


expense_folder = config.folders['expensemanager']

df_folder = get_folder_table(expense_folder)
file = search_file(df_folder, '.*master.*')
test_file = File(file_id=file['id'], name=file['name'])

app = FastAPI()


@app.get("/")
def root():
    return {"message": "to be or not to be"}


@app.get("/files")
def get_file_info_table() -> dict:

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


@app.get("/dump")
def dump_db():
    # Connect to the Postgres database
    conn = psycopg2.connect(
        host="postgres-db",
        port="5432",
        database="postgres",
        user="postgres",
        password="pg_pass"
    )

    # Create a cursor object
    cur = conn.cursor()

    # Execute the pg_dump command and save the output to a file
    with open(directories.root/"dump.sql", "w") as f:
        cur.copy_to(f, r"(SELECT pg_catalog.pg_tablespace_location(oid)||'/'||relfilenode||'.csv' FROM pg_class WHERE relkind='r' AND relnamespace='public')")

    # Close the cursor and connection
    cur.close()
    conn.close()


@app.get("/chart")
async def chart(offset: int=0):

    data = test_file.monthly_cumulative_expenses(accs=['Credit ENBD', 'AED ENBD', 'Cash AED', 'Capital AED'],
                                                     month_offset=offset)

    fig = plot_mom(data)

    # Return the PNG image as HTML
    png_output = yield_plot(fig)
    return Response(content=png_output.getvalue(), media_type="image/png")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
