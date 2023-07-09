import uuid
from typing import Tuple

import httpx
from httpx import Headers
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    id: str | None = None


class Tenant(BaseModel):
    id: uuid.UUID
    name: str


class Role(BaseModel):
    id: uuid.UUID
    name: str
    scopes: list[str]


class User(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    password_hash: str
    disabled: bool
    tenant: Tenant
    roles: list[Role]


def get_token(base_url: str, username: str, password: str, tenant: str) -> Tuple[Token, Headers]:
    res = httpx.post(
        f"{base_url}/tokens",
        data={'username': username, 'password': password, 'tenant': tenant}
    )
    res.raise_for_status()
    return Token(**res.json()), res.headers


def get_user(
        base_url: str,
        token: str,
) -> Tuple[User, Headers]:
    res = httpx.get(
        f"{base_url}/users/me",
        headers={'Authorization': f"Bearer {token}"},
        follow_redirects=True,
    )
    res.raise_for_status()
    return User(**res.json()), res.headers
