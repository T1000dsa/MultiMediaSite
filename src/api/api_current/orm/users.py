from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException

from src.core.config import settings
from src.core.schemas.users import UserRead, UserBase
from src.core.models.users import UserModel
from src.core.models.db_helper import db_helper

# Create user
async def create_user(
        session:AsyncSession,
        user_create:UserBase
) -> UserModel:
    user = UserModel(**user_create.model_dump())

    # This part can cause problem in future assosiated with performance
    stm = select(UserModel).where(UserModel.login==user_create.login)
    user_login = (await session.execute(stm)).scalar_one_or_none()
    if user_login: # Not none
        raise HTTPException(status_code=400, detail="Login already exists")
    # This part can cause problem in future assosiated with performance

    session.add(user)
    user.set_password()
    await session.commit()
    #await session.refresh(user)
    return user

# Give users
async def give_all_users(
        session:AsyncSession
) -> list[UserModel]:
    query = select(UserModel).order_by(UserModel.id)
    all_users = await session.execute(query)
    result = all_users.scalars().all()
    return result

async def give_one_user(
        session:AsyncSession,
        user_id:int
) -> UserModel|None:
    if user_id < 1:
        raise HTTPException(status_code=400, detail="Cant be less than 1.")
    result = await session.get(UserModel, user_id)
    if result:
        return result
    raise HTTPException(status_code=400, detail="There is no user with such id.")

