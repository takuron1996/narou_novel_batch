"""リクエスト関連の処理."""

import requests

from config.log import console_logger


def request_get(url, headers=None, payload=None, timeout=60):
    """Get通信した結果のレスポンスを返す.

    Parameters
    ----------
    url : str
        接続したいWebページのURL

    Returns:
    -------
    requests.Response
        取得したレスポンス情報を返す
    None
        正常通信できなかった場合
    """
    try:
        response = requests.get(
            url=url, params=payload, headers=headers, timeout=timeout
        )
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except requests.exceptions.RequestException as err:
        console_logger.warning(err)
        return None
