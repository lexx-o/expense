from dataclasses import dataclass
from config import config


@dataclass(frozen=True)
class Columns:
    DATE = config.schema.date
    ACC = config.schema.account
    AMOUNT = config.schema.amount
    CAT = config.schema.lvl1
    CAT2 = config.schema.lvl2
    DESC = config.schema.text

    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'


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
