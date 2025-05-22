from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import Optional

import logging

from src.core.config.config import templates, settings
from src.utils.prepared_response import prepare_template
from src.core.dependencies.auth_injection import GET_AUTH_SERVICE
from src.core.schemas.user import UserSchema


logger = logging.getLogger(__name__)
router = APIRouter(prefix=settings.prefix.api_data.prefix, tags=['auth'])


@router.get("/login")
async def html_login(
    request:Request,
    error:str|None = None,
    form_data:dict|None = {}
    ):

    prepared_data = {
        "title":"Sigh In",
        "template_action":settings.prefix.api_data.prefix+'/login/process',
        "form_data":form_data,
        "error":error
        }
    
    add_data = {
            "request":request
        }
    
    template_response_body_data = await prepare_template(
        data=prepared_data,
        additional_data=add_data
        )

    response = templates.TemplateResponse('users/login.html', template_response_body_data)
    return response


@router.post("/login/process")
async def login(
    request: Request,
    auth_service: GET_AUTH_SERVICE,
    login=Form(...), 
    password=Form(...)
):
    form_data={'login':login, 'password':password}
    try:
        session_token = await auth_service.authenticate_user(
            login=login,
            password=password
        )
        logger.debug(f'{session_token}')
        
        if not session_token:
            return await html_login(request=request, error='Invalid credentials', form_data=form_data)
        
        response = RedirectResponse(url='/', status_code=302)

        logger.debug(f'{response} {session_token.session_token}')

        response = await auth_service.set_session_cookies(response, session_token)
        
        return response
        
    except Exception as err:
        logger.error(f"Login failed: {err}")
        return await html_login(request=request, error='Login failed', form_data=form_data)

@router.get("/register")
async def html_register(
    request:Request
):
    logger.info('inside html_register')

    prepared_data = {
        "title":"Sigh Up",
        "template_action":settings.prefix.api_data.prefix+'/register/process',
        }
    
    add_data = {
            "request":request
        }
    

    template_response_body_data = await prepare_template(
        data=prepared_data,
        additional_data=add_data
        )
    
    response = templates.TemplateResponse('users/register.html', template_response_body_data)
    return response

@router.post("/register/process")
async def register(
    request:Request,
    auth_service: GET_AUTH_SERVICE,
    login: str = Form(...),
    password: str = Form(...),
    password_again: str = Form(...),
    username:str = Form(...),
    mail: str = Form(...),
    bio: str = Form(...)
    
):

    logger.info(f'User: {login} tries to registrate...')

    try:
        await auth_service.create_user(
        login=login,
        password=password,
        password_again=password_again,
        username=username,
        mail=mail,
        bio=bio)
 
    except IntegrityError as err:
        logger.info(f'{err}') 
        return "Such user already in database"

    except Exception as err:
        logger.error(f'{err}')
        raise err
    
    prepared_data = {
        "title":"Registration success",
        "content":"Registration was success!"
        }
    
    add_data = {
            "request":request
        }
    
    logger.info('success registration')
    template_response_body_data = await prepare_template(
        data=prepared_data,
        additional_data=add_data)
    return templates.TemplateResponse('users/register_success.html', template_response_body_data)


@router.get('/logout')
async def logout(
    auth_service: GET_AUTH_SERVICE
):
    response = RedirectResponse(url=router.prefix + "/login", status_code=status.HTTP_303_SEE_OTHER)
    
    try:
        response = await auth_service.logout_user(response=response)

    except Exception as e:
        logger.debug(f"Unexpected error: {e}")
    
    return response