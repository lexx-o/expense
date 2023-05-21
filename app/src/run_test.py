from config import config

from processing import get_folder_table, search_file, monthly_cumulative_expenses

from charts import plot_mom


if __name__ == '__main__':

    expense_folder = config.folders['expensemanager']

    df_folder = get_folder_table(expense_folder)

    trx_aed = search_file(df_folder, '.*aed.csv')
    trx_nonaed = search_file(df_folder, '.*infrequent.csv')
    trx_closed = search_file(df_folder, '.*closed.*.csv')

    expenses = monthly_cumulative_expenses(file=trx_aed,
                                           accs=['Credit ENBD', 'AED ENBD', 'Cash AED', 'Capital AED'],
                                           month_offset=-5)

    # fig = plot_mom(expenses)

    print('Done!')
