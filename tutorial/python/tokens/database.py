from datetime import datetime
from pysqlx_engine import PySQLXEngineSync, BaseRow
from pydantic import Field, Json
from uuid import UUID
from os import environ

QUARTILE_ID = "febdb7d2-e95d-11ed-9255-65636df51340"
"""
This is the id of the row that will be used to store the tokens.

This is a constant value and should not be changed.
"""


class TokenTable(BaseRow):
    id: UUID = QUARTILE_ID
    access_token: str
    access_token_expires: int
    refresh_token: str
    updating: bool
    json_data: Json
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TokenDB:
    def __init__(self):
        """
        getenv("DATABASE_URL") is used to get the database url
        from the environment variables.

        example: postgresql://USER:PASSWORD@HOST:PORT/DATABASE
        """
        self.uri = environ["DATABASE_URL"]
        self.db = PySQLXEngineSync(uri=self.uri)
        self.db.connect()

    def create_table(self):
        """
        Creating the table if it does not exist.
        """
        sql = """
            CREATE TABLE IF NOT EXISTS quartile_tokens (
                id UUID NOT NULL, 
                access_token TEXT, 
                refresh_token TEXT, 
                access_token_expires INTEGER, 
                updating BOOLEAN, 
                json_data JSON, 
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
                updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
                PRIMARY KEY (id)
            );
        """
        self.db.execute(sql=sql)

    def select_by_id(self, id: UUID) -> TokenTable:
        """
        Selecting a token by id from the database and
        returning it as an instance of the TokenTable class.
        """
        sql = "SELECT * FROM quartile_tokens WHERE id = :id;"
        return self.db.query_first(
            sql=sql,
            parameters={"id": id},
            model=TokenTable,
        )

    def insert(self, data: TokenTable) -> TokenTable:
        """
        Inserting tokens and json_data on the database.
        """
        sql = """
            INSERT INTO quartile_tokens (
                id,
                access_token,
                refresh_token,
                access_token_expires,
                updating,
                json_data,
                created_at,
                updated_at
            ) VALUES (
                :id,
                :access_token,
                :refresh_token,
                :access_token_expires,
                :updating,
                :json_data,
                :created_at,
                :updated_at
            );
        """
        params = data.dict()
        self.db.execute(sql=sql, parameters=params)
        return self.select_by_id(id=data.id)

    def update(self, data: TokenTable) -> TokenTable:
        """
        Updating tokens and json_data on the database.
        """
        sql = """
            UPDATE quartile_tokens SET
                access_token            = :access_token,
                refresh_token           = :refresh_token,
                access_token_expires    = :access_token_expires,
                updating                = :updating,
                json_data               = :json_data,
                updated_at              = :updated_at
            WHERE id                    = :id;
        """
        params = data.dict()
        self.db.execute(sql=sql, parameters=params)
        return self.select_by_id(id=data.id)

    def update_status(self, id: UUID, updating: bool) -> TokenTable:
        """
        Updating status is used to prevent multiple requests to the API.
        When updating is True, the API will not be called.
        """

        sql = """
            UPDATE quartile_tokens SET
                updating    = :updating,
                updated_at  = :updated_at
            WHERE id        = :id;
        """
        params = {"id": id, "updating": updating, "updated_at": datetime.now()}
        self.db.execute(sql=sql, parameters=params)
        return self.select_by_id(id=id)
