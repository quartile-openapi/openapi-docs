## About
The OAuth2 system is premised on having a token expiration process.

This can cause problems when you need to call a service asynchronously many times. In this period of time the access token may expire.

This tutorial provides a way to deal with this problem.

## Solving
1. **Database** to save the tokens.
2. **Worker** to update the refresh token when there is 5 minutes left to expire.
3. **Microservice** to provide the most up-to-date token.


## Using Python and PostgreSQL

This example uses Python with program language and DB PostgreSQL to save tokens.

## GitHub - All Code
[GitHub :material-github:](https://github.com/quartile-openapi/openapi-docs/tree/main/docs/python/tokens/){ .md-button }


## Install Dependencies

* **sqlalchemy**: ORM Database
* **psycopg2-binary**: Drive Database
* **httpx**: Client HTTP
* **pydantic**: Create model with validation

<div class="termy">

```console
$ pip install sqlalchemy psycopg2-binary httpx pydantic
Requirement already satisfied: sqlalchemy in ./.pyenv/versions/3.10.1/lib/python3.10/site-packages (1.4.36)
Collecting psycopg2-binary
  Downloading psycopg2_binary-2.9.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/3.0 MB 25.9 MB/s eta
...
...

```
</div>

## File Structure
* database.py
* schema.py
* access_token_consumer.py
* refresh_token_worker.py

---
**Common Files**
---

### **database.py**

**1.** Imports.
```Python hl_lines="4-6"
from datetime import datetime
from uuid import uuid1

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, declarative_base
```

**2.** Create Engine and Session.
```Python hl_lines="3-4"
database_uri = "postgresql+psycopg2://postgres:password@localhost:5432/fastapi_prisma"
# change echo to false to not show sql
engine = sqlalchemy.create_engine(database_uri, echo=True)
session = Session(bind=engine, autocommit=True, autoflush=True)
```

**3.** Create **declarative_base** for the mapping table.
```Python
Base = declarative_base()
```

**4.** Mapping table.
```Python
class Tokens(Base):
    __tablename__ = "quartile_tokens"
    id = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid1)
    access_token = sqlalchemy.Column(sqlalchemy.TEXT)
    refresh_token = sqlalchemy.Column(sqlalchemy.TEXT)
    access_token_expires = sqlalchemy.Column(sqlalchemy.DateTime)
    updating = sqlalchemy.Column(sqlalchemy.Boolean)
    json_data = sqlalchemy.Column(sqlalchemy.JSON)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.now, nullable=False
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.now, nullable=False, onupdate=datetime.now
    )
```

**5.** Create table.
```Python
Base.metadata.create_all(engine)
```
**Or** execute the SQL
```SQL
CREATE TABLE quartile_tokens (
    id UUID NOT NULL, 
    access_token TEXT, 
    refresh_token TEXT, 
    access_token_expires TIMESTAMP WITHOUT TIME ZONE, 
    updating BOOLEAN, 
    json_data JSON, 
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    PRIMARY KEY (id)
)
```

*Complete file*

=== ":fontawesome-brands-python: database.py"
``` python
from datetime import datetime
from uuid import uuid1

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()
# change to uri db
database_uri = "postgresql+psycopg2://postgres:password@localhost:5432/fastapi_prisma"
# change echo to false to not show sql
engine = sqlalchemy.create_engine(database_uri, echo=True)
session = Session(bind=engine, autocommit=True, autoflush=True)


class Tokens(Base):
    __tablename__ = "quartile_tokens"
    id = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid1)
    access_token = sqlalchemy.Column(sqlalchemy.TEXT)
    refresh_token = sqlalchemy.Column(sqlalchemy.TEXT)
    access_token_expires = sqlalchemy.Column(sqlalchemy.DateTime)
    updating = sqlalchemy.Column(sqlalchemy.Boolean)
    json_data = sqlalchemy.Column(sqlalchemy.JSON)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.now,
        nullable=False,
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.now,
        nullable=False,
        onupdate=datetime.now,
    )

Base.metadata.create_all(engine)
```

### **schema.py**

**1.** Imports.
```Python
from datetime import datetime
from pydantic import BaseModel
```

**2.** Models.
```Python
class Authorization(BaseModel):
    token: str
    type: str
    expires_in: int
    expires_at: datetime
    not_before: int
    note: str


class Refresh(BaseModel):
    token: str
    expires_in: int
    expires_at: datetime
    note: str


class AuthToken(BaseModel):
    authorization: Authorization
    refresh: Refresh
```

*Complete file*

=== ":fontawesome-brands-python: schema.py"
``` python
from datetime import datetime

from pydantic import BaseModel


class Authorization(BaseModel):
    token: str
    type: str
    expires_in: int
    expires_at: datetime
    not_before: int
    note: str


class Refresh(BaseModel):
    token: str
    expires_in: int
    expires_at: datetime
    note: str


class AuthToken(BaseModel):
    authorization: Authorization
    refresh: Refresh

```

---
**Refresh Token and Access Token**
---
### **refresh_token_worker.py**


**1.** Imports.
```Python hl_lines="6-7"

from datetime import datetime, timedelta
from time import sleep

import httpx

from database import Tokens, session
from schema import AuthToken

```

**2.** Create function to get new refresh token.
```Python
def get_new_refresh_token(refresh_token: str):
    uri = "https://api.quartile.com/auth/v1/refresh-token"
    body = {"refresh_token": refresh_token}
    resp = httpx.post(url=uri, json=body)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    return AuthToken.parse_obj(data), data
```

**3.** Create function to get new refresh token.

This function loops for two hours, every minute it checks if the access_token has expired.

If it has expired, it changes its status to update.

After changing the status, a request is made for a new set of tokens and updates.

```Python hl_lines="10-13 23-24"
def main(max_sec: int = 3600 * 2):
    # run 120 times in 2 hours
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
```
**4.** Run code.
```sh
python refresh_token_worker.py
```

*Complete file*

=== ":fontawesome-brands-python: refresh_token_worker.py"
``` python
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
```

### **access_token_consumer.py**

**1.** Imports.
```Python hl_lines="3-4"
from time import sleep

from database import Tokens, session
from schema import AuthToken
```

**2.** Create function to get access token.
```Python 
def get_access_token():
    while True:
        result: Tokens = session.query(Tokens).filter(Tokens.updating != True).first()
        if result:
            session.close()
            return AuthToken.parse_obj(result.json_data)
        # waiting for token update.
        sleep(1.5)

if __name__ == "__main__":
    data = get_access_token()
    print(data)
```

**3.** Run code.
```sh
python access_token_consumer.py
```

*Complete file*

=== ":fontawesome-brands-python: refresh_token_worker.py"

```python
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
    data = get_access_token()
    print(data)

```