from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from typing import Annotated

from travelothai.core import deps
from travelothai.models import user_model, get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(current_user: user_model.User = Depends(deps.get_current_user)) -> user_model.User:
    return current_user


@router.get("/{user_id}")
async def get(
    user_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: user_model.User = Depends(deps.get_current_user),
) -> user_model.User:

    user = await session.get(user_model.DBUser, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    return user


@router.post("/create")
async def create(
    user_info: user_model.RegisteredUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> user_model.User:

    result = await session.exec(
        select(user_model.DBUser).where(user_model.DBUser.username == user_info.username)
    )

    user = result.one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is exists.",
        )

    user = user_model.DBUser.model_validate(user_info)
    await user.set_password(user_info.password)
    session.add(user)
    await session.commit()

    return user


@router.put("/{user_id}/change_password")
async def change_password(user_id: str,
    password_update: user_model.ChangedPassword,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: user_model.User = Depends(deps.get_current_user),
) -> dict:

    result = await session.get(user_model.DBUser, user_id)

    user = result.one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )

    if not user.verify_password(password_update.current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    user.set_password(password_update.new_password)
    session.add(user)
    await session.commit()


@router.put("/{user_id}/update")
async def update(
    request: Request,
    user_id: str,
    user_update: user_model.UpdatedUser,
    password_update: user_model.ChangedPassword,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: user_model.User = Depends(deps.get_current_user),
) -> user_model.User:

    db_user = await session.get(user_model.DBUser, user_id)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )

    if not db_user.verify_password(password_update.current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    db_user.sqlmodel_update(user_update)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user