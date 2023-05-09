from enum import Enum


class Columns:
    DATE = 'Date'
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    AMOUNT = 'Amount'
    CAT = 'Category'
    ACC = 'Account'


class Accs(Enum):
    ENBD = 'AED ENBD'
    CREDIT_ENBD = 'Credit ENBD'
    CASH = 'Cash AED'
    CAPITAL = 'Capital AED'
    ADVCLUB = 'AED AdvClub'


class AccGroup(Enum):
    AED = [Accs.ENBD, Accs.CREDIT_ENBD, Accs.CASH, Accs.CAPITAL, Accs.ADVCLUB]
