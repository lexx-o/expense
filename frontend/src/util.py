import pandas as pd
import requests
import json


def df_from_endpoint(url: str) -> pd.DataFrame:
    """
    Returns DataFrame from dict, yielded from backend endpoint
    Args:
        url: endpoint URL

    Returns:
        pd.DataFrame
    """
    resp = requests.get(url)
    df = pd.read_json(resp.content.decode('utf-8'))
    return df


def data_from_endpoint(url: str):
    """
        Returns payload from backend endpoint
        Args:
            url: endpoint URL
        Returns:
            pd.DataFrame
        """
    resp = requests.get(url)
    data_string = resp.content.decode('utf-8')
    return json.loads(data_string)
