from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import Optional

import logging

from src.core.config.config import auth_prefix
from src.core.dependencies.auth_injection import GET_AUTH_SERVICE, GET_CURRENT_USER
from src.api.v1.utils.render import render_login_form, render_register_form, render_profile_form


logger = logging.getLogger(__name__)
router = APIRouter(prefix=auth_prefix, tags=['auth'])


@router.get("/login")
@router.post("/login")
async def handle_login(
    request: Request,
    auth_service: GET_AUTH_SERVICE,
    login: str = Form(None),  # Optional for POST
    password: str = Form(None),  # Optional for POST
    errors: str = None,  # For error passing
):
    # Handle POST request (form submission)
    if request.method == "POST":
        form_data = {'login': login, 'password': password}
        try:
            session_token = await auth_service.authenticate_user(
                login=login,
                password=password
            )
            
            if not session_token:
                return await render_login_form(
                    request, 
                    errors='Invalid credentials', 
                    form_data=form_data
                )
            
            response = RedirectResponse(url='/', status_code=302)
            return await auth_service.set_session_cookies(response, session_token)
            
        except Exception as err:
            logger.error(f"Login failed: {err}")
            return await render_login_form(
                request, 
                errors='Login failed', 
                form_data=form_data
            )

    # Handle GET request (initial form display)
    return await render_login_form(request)


@router.get("/register")
@router.post("/register")
async def handle_register(
    request: Request,
    auth_service: GET_AUTH_SERVICE,
    login: str = Form(None),
    password: str = Form(None),
    password_again: str = Form(None),
    username: str = Form(None),
    email: str = Form(None),
    bio: str = Form(None),
    errors: str = None
):
    # Handle POST request (form submission)
    if request.method == "POST":
        logger.info(f'User: {login} tries to register...')
        
        try:
            await auth_service.create_user(
                login=login,
                password=password,
                password_again=password_again,
                username=username,
                email=email,
                bio=bio
            )
            
            # Successful registration - redirect to login
            return RedirectResponse(url=f"{auth_prefix}/login?registered=true", status_code=303)
            
        except IntegrityError as err:
            logger.info(f'{err}')
            return await render_register_form(
                request,
                errors='Username or email already exists',
                form_data={
                    'login': login,
                    'username': username,
                    'email': email,
                    'bio': bio
                }
            )
            
        except Exception as err:
            logger.error(f'{err}')
            return await render_register_form(
                request,
                errors='Registration failed. Please try again.',
                form_data={
                    'login': login,
                    'username': username,
                    'email': email,
                    'bio': bio
                }
            )

    # Handle GET request (initial form display)
    return await render_register_form(request, errors=errors)

@router.get('/logout')
async def logout(
    auth_service: GET_AUTH_SERVICE
):
    response = RedirectResponse(url=auth_prefix + "/login", status_code=status.HTTP_303_SEE_OTHER)
    
    try:
        response = await auth_service.logout_user(response=response)

    except Exception as e:
        logger.debug(f"Unexpected error: {e}")
    
    return response

@router.get('/profile')
async def profile(request:Request, curr_user:GET_CURRENT_USER):
    if curr_user:
        return await render_profile_form(request, curr_user)
    #return HTTPException(detail='Unauthorized', status_code=status.HTTP_401_UNAUTHORIZED)