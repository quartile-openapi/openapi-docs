from datetime import datetime
from pydantic import BaseModel as _BaseModel, Field

class BaseModel(_BaseModel):
    class Config:
        orm_mode = True
        ignore_extra = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Authorization(BaseModel):
    token: str
    type: str
    expires_in: int = Field(..., alias="expiresIn")
    expires_at: datetime = Field(..., alias="expiresAt")
    not_before: int = Field(..., alias="notBefore")
    note: str


class Refresh(BaseModel):
    token: str
    expires_in: int = Field(..., alias="expiresIn")
    expires_at: datetime = Field(..., alias="expiresAt")
    note: str


class AuthToken(BaseModel):
    authorization: Authorization
    refresh: Refresh
