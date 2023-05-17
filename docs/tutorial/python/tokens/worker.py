from datetime import datetime, timedelta
import logging

import httpx
from os import environ
from database import QUARTILE_ID, TokenDB, TokenTable
from schema import AuthToken

logging.basicConfig(level=logging.INFO)

# This is the base uri for the Quartile API.
BASE_URI = "https://api.quartile.com/auth/v2"
# set your subscription key in your environment variables,
# You can find your subscription key in the Developer Portal.
SUBSCRIPTION_KEY = environ["QUARTILE_SUBSCRIPTION_KEY"]
# set your username(email) in your environment variables, the same used in the Portal
USERNAME = environ["QUARTILE_YOUR_USERNAME"]
# set your password in your environment variables, the same used in the Portal
PASSWORD = environ["QUARTILE_YOUR_PASSWORD"]


# HTTP - API
def login() -> AuthToken:
    uri = f"{BASE_URI}/login"
    body = {"username": USERNAME, "password": PASSWORD}
    headers = {"Subscription-Key": SUBSCRIPTION_KEY}
    resp = httpx.post(url=uri, json=body, headers=headers, timeout=10)

    logging.info(f"login... return status code: {resp.status_code}")
    assert resp.status_code == 201, resp.text

    data = resp.json()
    return AuthToken.parse_obj(data)


def refresh_tokens(refresh_token: str) -> AuthToken:
    uri = f"{BASE_URI}/refresh"
    body = {"token": refresh_token}
    headers = {"Subscription-Key": SUBSCRIPTION_KEY}
    resp = httpx.post(url=uri, json=body, headers=headers, timeout=10)

    logging.info(f"refreshing tokens... return status code: {resp.status_code}")
    assert resp.status_code == 201, resp.text

    data = resp.json()
    return AuthToken.parse_obj(data)


# DATABASE - POSTGRES
def insert_token(db: TokenDB):
    tokens = login()

    data = TokenTable(
        id=QUARTILE_ID,
        access_token=tokens.authorization.token,
        access_token_expires=tokens.authorization.expires_at.timestamp(),
        refresh_token=tokens.refresh.token,
        updating=False,
        json_data=tokens.json(),
    )

    db.insert(data=data)
    logging.info("tokens inserted")


def update_token(db: TokenDB, row: TokenTable):
    # get new set of tokens
    try:
        tokens = refresh_tokens(refresh_token=row.refresh_token)
        logging.info("tokens refreshed")
    except AssertionError:
        # if the refresh token is expired, then make a 
        # login request to get a new set of tokens.
        logging.info("refresh token expired, getting new tokens...")
        tokens = login()
        logging.info("tokens refreshed")

    data = TokenTable(
        id=QUARTILE_ID,
        access_token=tokens.authorization.token,
        access_token_expires=tokens.authorization.expires_at.timestamp(),
        refresh_token=tokens.refresh.token,
        updating=False,
        json_data=tokens.json(),
    )

    # update tokens
    db.update(data=data)
    logging.info("tokens updated")


# MAIN
def main():
    logging.info("starting worker...")
    # create a new instance of TokenDB class
    db = TokenDB()

    # try create quartile_tokens table if not exists,
    # you can remove this line if you already have the table
    db.create_table()

    # get one row if the QUARTILE_ID is equal to the id column
    row = db.select_by_id(id=QUARTILE_ID)

    # case the row is None, then make a login request to get a new set of tokens.
    if row is None:
        logging.info("inserting tokens...")
        insert_token(db=db)
        return  # exit the function

    # get datetime utc now minus 1 hour
    now = int((datetime.utcnow() - timedelta(hours=1)).timestamp())

    # check if the access_token_expires is greater than or equal now minus 5

    if row.access_token_expires <= now:
        logging.info("updating tokens...")
        # change status to updating
        # this will prevent the consumer function to get the invalid token
        db.update_status(id=QUARTILE_ID, updating=True)

        # try to update the tokens
        update_token(db=db, row=row)


if __name__ == "__main__":
    main()
