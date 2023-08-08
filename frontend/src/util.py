import requests
from requests.exceptions import ConnectionError
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
