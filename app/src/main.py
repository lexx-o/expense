from fastapi import FastAPI
import logging
import uvicorn

from config import config
from dbio import Table, update_account_data_in_table
from driveio import get_file, get_folder_table
from processing import prepare_monthly_cumulative_expenses, prepare_balance_table


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

expense_folder = config.folders.expensemanager
master_table = Table(name='master', schema='public')

app = FastAPI()


@app.get("/")
def root() -> dict:
    """No functionality implemented on root"""
    return {'status': 'healthy'}


@app.get("/test")
def test() -> dict:
    """Test endpoint"""
    return {'msg': 'test-value'}


@app.get("/monthly-expense-table")
async def get_monthly_expense_table() -> dict:
    """Get data for monthly expense chart"""
    df = prepare_monthly_cumulative_expenses(master_table)
    return df.to_dict()


@app.get("/balance-table")
async def get_balance_table() -> dict:
    """Get data for historic balance chart"""
    df = prepare_balance_table(master_table)
    return df.to_dict()


@app.get("/file-list")
async def get_file_list() -> dict:
    """List files in expense folder on Google Drive"""
    folder = get_folder_table(expense_folder)
    return folder.to_dict()


@app.get("/update-db-with-file")
def update_db_with_file(id: str) -> dict:
    """Upload selected file from Google Drive to DB
        Args:
            id: file id on Google Drive"""
    folder = get_folder_table(expense_folder)
    file = get_file(folder, id=id)
    update_account_data_in_table(data=file.data, table=master_table)
    return {'status': 'success',
            'id': id,
            'filename': file.name,
            'shape': file.data.shape
            }


if __name__ == '__main__':
    logger.info('STARTING SERVER')
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
