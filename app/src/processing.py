from datetime import date

import pandas as pd

from config.variables import Columns

pd.set_option('mode.chained_assignment', None)


def prepare_monthly_cumulative_expenses(df_expense: pd.DataFrame) -> pd.DataFrame:

    df_expenses_daily = df_expense.groupby(by=Columns.DATE).sum()[[Columns.AMOUNT]]

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
