from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, join
from typing import Optional
import logging 

from src.core.services.database.models.users import UserModel
from src.core.schemas.user import UserSchema


logger = logging.getLogger(__name__)

async def select_data_user_id(
        session: AsyncSession,
        user_id:int
        ) -> Optional[UserModel]:
    try:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        data_user =  result.scalar_one_or_none()

        if not data_user: # if data_user is none its will raise an error
            return None
        return data_user
    
    except Exception as err:
        logger.error(f"Failed to select user data: {str(err)}")
        raise err

async def select_data_user(
    session: AsyncSession,
    login: str,
    password: str
) -> Optional[UserModel]:
    logger.debug('inside select_data_user')
    try:
        query = select(UserModel).where(UserModel.login == login)
        result = await session.execute(query)
        data_user =  result.scalar_one_or_none()
        if not data_user: # if data_user is none it's will raise an error further
            return None
        else:
            if data_user.check_password(password): # if password is validates properly user returns and return None in any else cases
                logger.debug(f"User {data_user.login} was authorized")
                return data_user
    
    except Exception as err:
        logger.error(f"Failed to select user data: {str(err)}")
        raise err
    
async def select_user_email(
    session: AsyncSession,
    email: str
    ) -> Optional[UserModel]:
    try:
        query = select(UserModel).where(UserModel.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    except ValueError as err:
        logger.error(f"select_user_email doesn't support such method {type(email)} {str(err)}")
        raise err
    
    except Exception as err:
        logger.error(f"Failed to select user data: {str(err)}")
        raise err

async def insert_data(session:AsyncSession, **kwargs) -> None:
    try:
        res = UserSchema.model_validate(UserSchema(**kwargs), from_attributes=True)
        user_data = {i: k for i, k in res.model_dump().items() if i != 'password_again'}
        new_data = UserModel(**user_data)
        new_data.set_password() # plain text password -> hashed password
        session.add(new_data)
        await session.commit()
        await session.refresh(new_data)  # Refresh to get any database-generated values
        logger.debug('User creation has been successfully completed')
        return new_data

    except IntegrityError as err:
        logger.info(f'{err}') 
        await session.rollback()
        raise err
            
    except Exception as e:
        logger.error(f'Error creating user: {e}')
        await session.rollback()
        raise e


async def delete_data(session:AsyncSession, user_id:int) -> None:
    try:
        query = (delete(UserModel).where(UserModel.id == user_id)) 
        await session.execute(query)
        await session.commit()

    except Exception as e:
        logger.error(f'Error deleting user: {e}')
        await session.rollback()
        raise e

async def user_activate(session:AsyncSession, user_id:int, activate:bool) -> Optional[UserModel]:
    try:
        query = select(UserModel).where(UserModel.id == user_id)
        user = (await session.execute(query)).scalar_one_or_none()

        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        
        user.is_active = activate
        await session.commit()
        await session.refresh(user)
        return user
    
    except Exception as e:
        logger.error(f'Error deleting user: {e}')
        await session.rollback()
        raise e