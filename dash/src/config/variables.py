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
    SAVINGS = 'Deposit AED'


@dataclass(frozen=True)
class AccGroup:
    # order dependent
    AED = [
        Accs.SAVINGS,
        Accs.ENBD,
        Accs.CAPITAL,
        Accs.ADVCLUB,
        Accs.CASH,
        Accs.AED_AR,
        Accs.CREDIT_ENBD
    ]


figure_layout = dict(
    height=600,
    margin=dict(
        l=20,
        r=20,
        b=20,
        t=20,
        pad=4
    ),
    hovermode='x',

    font=dict(
        size=14,
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(210,210,210,0.8)',
)
