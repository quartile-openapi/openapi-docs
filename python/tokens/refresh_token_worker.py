from datetime import datetime, timedelta
from time import sleep

import httpx

from database import Tokens, session
from schema import AuthToken


def get_new_refresh_token(refresh_token: str):
    uri = "https://api.quartile.com/auth/v1/refresh-token"
    body = {"refresh_token": refresh_token}
    resp = httpx.post(url=uri, json=body)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    return AuthToken.parse_obj(data), data


# max_sec 3600 = 1 hour
def main(max_sec: int = 3600 * 2):
    # run 120 times in 2 hours
    """
        Get one row if the access_token_expires is greater than or equal now minus 5
        for example:
          access_token_expires: 2022-06-10 13:51:44.000000
          timestamp:            2022-06-10 13:52:44.000000
        access_token_expires <= timestamp -> TRUE
        THEN UPDATE TOKEN
    Args:
        max_sec (int, optional): _description_. Defaults to 3600*2.
    """
    for _ in range(0, max_sec, 60):
        # get date and time from now minus 5 minutes
        now = str(datetime.utcnow() - timedelta(minutes=5))
        result: Tokens = (
            session.query(Tokens).filter(Tokens.access_token_expires <= now).first()
        )
        if result:
            # change status to updating
            session.query(Tokens).filter(Tokens.id == result.id).update(
                values={"updating": True}
            )

            # get new set of tokens
            tokens, data = get_new_refresh_token(refresh_token=result.refresh_token)
            values = {
                "access_token": tokens.authorization.token,
                "access_token_expires": tokens.authorization.expires_at,
                "refresh_token": tokens.refresh.token,
                "updating": False,
                "json_data": data,
            }
            # update tokens
            session.query(Tokens).filter(Tokens.id == result.id).update(values=values)

        sleep(60)
    session.close()


if __name__ == "__main__":
    main()
