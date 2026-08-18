import logging
from time import sleep

from database import QUARTILE_ID, TokenDB
from schema import AuthToken

logging.basicConfig(level=logging.INFO)


def get_access_token() -> AuthToken:
    """
    Gets an access token from the TokenDB.

    This function continuously checks the TokenDB for an available access
    token by calling the select_by_status method of the TokenDB class.

    If an access token is found, it is returned as an instance of the AuthToken class.
    If no access token is found, the function waits for 5 seconds and tries again.

    Returns:
        AuthToken: An instance of the AuthToken class representing the Quartile token.

    """
    while True:
        logging.info("getting token...")
        resp = TokenDB().select_by_id(id=QUARTILE_ID)

        # check if resp is not None and resp.updating is False
        if resp and resp.updating is False:
            logging.info("token found.")
            return AuthToken.parse_obj(resp.json_data)

        logging.info("token not found ot updating, waiting 5 seconds...")
        sleep(5)


if __name__ == "__main__":
    data = get_access_token()
    logging.info(data.json(indent=4))
