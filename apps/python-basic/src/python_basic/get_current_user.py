from typing import Annotated
from fastapi import Depends, Header, HTTPException
from pydantic import BaseModel


class CurrentUser(BaseModel):
    user_id: str
    tenant_id: str
    roles: list[str]


async def get_current_user(
    x_user_id: Annotated[str | None, Header()] = None,
    x_tenant_id: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    if not x_tenant_id or not x_user_id:
        raise HTTPException(status_code=401, detail="missing user headers")
    return CurrentUser(user_id=x_user_id, tenant_id=x_tenant_id, roles=["user"])
