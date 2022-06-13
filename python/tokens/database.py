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


# create table
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
# or execute the sql
"""
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
"""

# INSERT THE FIRST LINE BEFORE EXECUTING OTHER CODES.
"""
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
    '77be627a-e8b6-11ec-af7f-00155d0fb6c9',
    'dhfburrf',
    'dgwefrgeg',
    2022-06-10 13:51:44.000000,
    false,
    '{...add payload here}',
    '2022-06-10 13:51:44.000000',
    '2022-06-10 13:51:44.000000'
)
"""
