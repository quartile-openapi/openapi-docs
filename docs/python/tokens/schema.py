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
