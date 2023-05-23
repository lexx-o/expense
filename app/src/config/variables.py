from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class Columns:
    DATE = 'Date'
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    AMOUNT = 'Amount'
    CAT = 'Category'
    ACC = 'Account'


@dataclass(frozen=True)
class Accs:
    ENBD = 'AED ENBD'
    CREDIT_ENBD = 'Credit ENBD'
    CASH = 'Cash AED'
    CAPITAL = 'Capital AED'
    ADVCLUB = 'AED AdvClub'
    AED_AR = 'Nadya - AED'


@dataclass(frozen=True)
class AccGroup:
    AED = [Accs.ENBD, Accs.CREDIT_ENBD, Accs.CASH, Accs.CAPITAL, Accs.ADVCLUB, Accs.AED_AR]
