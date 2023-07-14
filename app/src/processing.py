from datetime import date

import pandas as pd

from config.variables import Columns, AccGroup
from dbio import Table

pd.set_option('mode.chained_assignment', None)


def prepare_monthly_cumulative_expenses(table: Table) -> pd.DataFrame:
    """Prepares dataset for monthly cumulative expenses line-chart from Table class"""
    df_raw = table.read(columns=[Columns.DATE, Columns.ACC, Columns.CAT, Columns.AMOUNT])
    df_raw = df_raw[df_raw[Columns.ACC].isin(AccGroup.AED)]
    df_raw = df_raw[~df_raw[Columns.CAT].isin(['Income', 'Account Transfer'])]

    df_expenses_daily = df_raw.groupby(by=Columns.DATE).sum()[[Columns.AMOUNT]]

    date_range = pd.date_range(df_expenses_daily.index.min(), df_expenses_daily.index.max())
    df_expenses_daily = df_expenses_daily.reindex(date_range, fill_value=0)

    df_expenses_daily[Columns.AMOUNT] *= -1
    df_expenses_daily[Columns.DAY] = df_expenses_daily.index.day

    df_expenses_daily['_period_id'] = df_expenses_daily.index.month + df_expenses_daily.index.year * 12
    df_expenses_daily['offset'] = df_expenses_daily['_period_id'] - (date.today().month + date.today().year * 12)
    df_expenses_daily['runtot'] = df_expenses_daily[['offset', Columns.AMOUNT]].groupby('offset').cumsum()

    df_expenses_daily['period'] = \
        df_expenses_daily.index.year.astype(str) \
        + "-" \
        + df_expenses_daily.index.month.astype(str)

    return df_expenses_daily[[Columns.DAY, 'period', 'offset', 'runtot']]


def prepare_balance_table(table: Table) -> pd.DataFrame:
    """Prepares dataset for stacked area chart depicting daily account balances"""

    df_raw = table.read(columns=[Columns.DATE, Columns.ACC, Columns.AMOUNT])
    df_raw = df_raw[df_raw[Columns.ACC].isin(AccGroup.AED)]

    # fill in values in daily gaps
    chunks = []
    for acc in df_raw[Columns.ACC].unique():
        chunk = df_raw[df_raw[Columns.ACC] == acc]
        chunk = chunk.groupby(by=Columns.DATE).sum()
        date_range = pd.date_range(start=chunk.index.min(), end=date.today())
        chunk = chunk.reindex(date_range, fill_value=0)
        chunk[Columns.ACC] = acc
        chunks.append(chunk)

    df = pd.concat(chunks, axis=0)
    df.reset_index(inplace=True)
    df.rename({'index': Columns.DATE}, axis=1, inplace=True)
    df.sort_values(by=[Columns.ACC, Columns.DATE], inplace=True)

    df = df.groupby(by=[Columns.ACC, Columns.DATE], as_index=False).sum()
    df['Balance'] = df.groupby(by=Columns.ACC)[Columns.AMOUNT].cumsum()

    return df[[Columns.DATE, Columns.ACC, 'Balance']]
