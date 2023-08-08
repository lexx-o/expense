import pandas as pd
import requests
import json


def request_from_endpoint(url: str) -> dict:
    """
        Returns a dict with
        from dict, yielded from backend endpoint
        Args:
            url: endpoint URL

        Returns:
            dict:
                status: [0, 1] 0 if status code 200, 1 in all other cases
                data: [dict] payload string if status code 200, error message in other cases
        """
    try:
        resp = requests.get(url)
    except ConnectionError as e:
        return {"status": 1,
                "data": {"message": f"Error: {e}"}
                }

    if resp.status_code == 200:
        return {"status": 0,
                "data": json.loads(resp.content.decode('utf-8'))}
    else:
        return {"status": 1,
                "data": {"message": f"Status code {resp.status_code}"}
                }


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
