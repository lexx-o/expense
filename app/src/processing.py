from datetime import date, timedelta

import pandas as pd

from driveio import _download_file, _load_folder
from config.variables import Columns

from dataclasses import dataclass


pd.set_option('mode.chained_assignment', None)


def get_folder_table(folder: str) -> pd.DataFrame:

    files_table = pd.DataFrame(_load_folder(folder=folder))

    if 'modifiedTime' in files_table.columns:
        files_table['modifiedTime'] = pd.to_datetime(files_table['modifiedTime'])
        files_table.sort_values(by='modifiedTime', ascending=False, inplace=True)

    return files_table


def search_file(folder: pd.DataFrame, name: str) -> dict:

    filtered = folder[folder['name'].str.contains(name)]
    file = filtered.sort_values(by='modifiedTime', ascending=False).iloc[0]
    file = dict(file)

    return file

@dataclass
class File:

    id: str
    name: str

    def _format_dataframe(self):
        self.data[Columns.DATE] = pd.to_datetime(self.data[Columns.DATE])
        self.data[Columns.AMOUNT].replace(to_replace='-', value='0', inplace=True)
        self.data[Columns.AMOUNT] = self.data[Columns.AMOUNT].astype('float')

    def __post_init__(self):
        iostream = _download_file(file_id=self.id)
        iostream.seek(0)
        self.data = pd.read_csv(iostream)
        self._format_dataframe()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'File ({self.name}, {self.id}, r/c: {self.data.shape})'

    def monthly_cumulative_expenses(self, accs: list, month_offset=0):
        df = self.data[self.data[Columns.ACC].isin(accs)]

        start = date.today() + pd.tseries.offsets.MonthBegin(-2 + month_offset)
        end = date.today() + pd.tseries.offsets.MonthEnd(month_offset)

        grid = pd.DataFrame(pd.date_range(start, end), columns=[Columns.DATE])

        df_expense = df[~df[Columns.CAT].isin(['Income', 'Account Transfer'])]
        df_expense[Columns.AMOUNT] = df[Columns.AMOUNT] * -1

        df_month = grid.merge(df_expense.groupby(Columns.DATE).sum()[Columns.AMOUNT].reset_index(), on=['Date'], how='left')
        df_month.fillna(0, inplace=True)

        df_month['month'] = df_month[Columns.DATE].dt.month
        df_month['day'] = df_month[Columns.DATE].dt.day

        df_month['runtot'] = df_month[['month', Columns.AMOUNT]].groupby('month').cumsum()

        df_month.loc[df_month['month'] == end.month, 'period'] = 'current'
        df_month.loc[df_month['month'] == start.month, 'period'] = 'previous'

        return df_month
