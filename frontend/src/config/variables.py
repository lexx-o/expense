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
