
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.config import settings
from src.core.schemas.users import UserRead, UserBase
from src.core.models.users import UserModel

# Create user
async def create_user(
        session:AsyncSession,
        user_create:UserBase
) -> UserModel:
    user = UserModel(**user_create.model_dump())
    session.add(user)
    await session.commit()
    #await session.refresh(user)
    return user

# Give users
async def give_all_users(
        session:AsyncSession
) -> list[UserModel]:
    query = select(UserModel)
    all_users = await session.execute(query)
    result = all_users.scalars().all()
    return result

async def give_one_user(
        session:AsyncSession,
        user_read:UserRead
) -> UserModel:
    query = select(UserModel).where(UserModel.id==user_read.id)
    all_users = await session.execute(query)
    result = all_users.scalar_one_or_none()
    return result