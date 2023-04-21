from time import sleep

from database import Tokens, session
from schema import AuthToken


def get_access_token():
    while True:
        result: Tokens = session.query(Tokens).filter(Tokens.updating != True).first()
        if result:
            session.close()
            return AuthToken.parse_obj(result.json_data)
        # waiting for token update.
        sleep(1.5)


if __name__ == "__main__":
    print("getting token...")
    data = get_access_token()
    print(data)
