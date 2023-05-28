import pandas as pd


def trim_date_and_remove_tz(dates: pd.Series, trim: 'str' = 's') -> pd.Series:
    dates1 = pd.to_datetime(dates)
    dates2 = dates1.dt.tz_localize(None)
    dates3 = dates2.dt.round(trim)
    return dates3
