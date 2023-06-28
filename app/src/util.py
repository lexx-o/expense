import pandas as pd


def trim_date_and_remove_tz(dates: pd.Series, trim: 'str' = 's') -> pd.Series:
    """
    Transforms a Series of date-like data into timezone-naive pd.Timestamp type and rounds to seconds
    Args:
        dates: Series containing dates
        trim: rounding period
    Returns:
        Series of pd.Timestamp data
    """
    dates1 = pd.to_datetime(dates)
    dates2 = dates1.dt.tz_localize(None)
    dates3 = dates2.dt.round(trim)
    return dates3
