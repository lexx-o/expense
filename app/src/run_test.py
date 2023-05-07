from config import config

from processing import get_folder_table, search_file, File

from charts import plot_mom


if __name__ == '__main__':

    expense_folder = config.folders['expensemanager']

    df_folder = get_folder_table(expense_folder)

    file = search_file(df_folder, '.*master.*')

    test_file = File(id=file['id'], name=file['name'])

    expenses = test_file.monthly_cumulative_expenses(accs=['Credit ENBD', 'AED ENBD', 'Cash AED', 'Capital AED'], month_offset=-5)

    fig = plot_mom(expenses)

    print('Done!')
