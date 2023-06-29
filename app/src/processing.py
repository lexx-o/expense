from datetime import date

import pandas as pd

from config.variables import Columns, AccGroup

pd.set_option('mode.chained_assignment', None)


def monthly_cumulative_expenses(data, month_offset=0):

    start = date.today() + pd.tseries.offsets.MonthBegin(-2 + month_offset)
    end = min(date.today() + pd.tseries.offsets.MonthEnd(month_offset), pd.Timestamp(date.today()))

    grid = pd.DataFrame(pd.date_range(start, end), columns=[Columns.DATE])

    df_expense = data[~data[Columns.CAT].isin(['Income', 'Account Transfer'])]
    df_expense.dropna(subset=['Amount'], inplace=True)
    df_expense[Columns.AMOUNT] = data[Columns.AMOUNT] * -1

    df_month = grid.merge(df_expense.groupby(Columns.DATE).sum()[Columns.AMOUNT].reset_index(),
                          on=['Date'], how='left')
    df_month.fillna(0, inplace=True)

    df_month['month'] = df_month[Columns.DATE].dt.month
    df_month['day'] = df_month[Columns.DATE].dt.day

    df_month['runtot'] = df_month[['month', Columns.AMOUNT]].groupby('month').cumsum()

    df_month.loc[df_month['month'] == end.month, 'period'] = 'current'
    df_month.loc[df_month['month'] == start.month, 'period'] = 'previous'

    return df_month


