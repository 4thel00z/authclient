from typing import Tuple

import httpx
from httpx import Headers
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    id: str | None = None


class User(BaseModel):
    username: str
    id: str | None = None
    tenant: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None


def get_token(base_url: str, username: str, password: str) -> Tuple[Token, Headers]:
    res = httpx.post(
        f"{base_url}/token",
        data={'username': username, 'password': password}
    )
    res.raise_for_status()
    return Token(**res.json()), res.headers


def get_user(
        base_url: str,
        token: str,
) -> Tuple[User, Headers]:
    res = httpx.get(
        f"{base_url}/users/me",
        headers={'Authorization': f"Bearer {token}"}
    )
    res.raise_for_status()
    return User(**res.json()), res.headers
