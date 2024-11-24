import re
from typing import Annotated
from fastapi import Request, Depends, Form, HTTPException, status, Cookie, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from datetime import timedelta
from database import SessionDep
from fastapi.security import OAuth2PasswordRequestForm
from configs import templates
from sqlmodel import select
from auth.schemas import Page, PaginationInput, User
from auth.models import UserPasswordUpdate, UserCreate, UserUpdate
from auth.dependencies import (
    get_current_active_user, 
    get_current_user, 
    get_password_hash,
    verify_password,
    create_access_token,
    change_user_password,
    update_user_profile,
    update_user_username,
    create_user,
    verify_first_name,
    verify_email,
    verify_last_name,
    verify_username,
    verify_password_strength,
    authenticate_user,
    get_user_generated_history,
    get_image_alt_text,
    get_all_users,
    paginate,
    PaginationDep,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter()

# read_users_me -> get_current_active_user -> get_current_user -> get_user
@router.get("/profile", response_class=HTMLResponse)
async def read_users_me(request: Request, current_user: Annotated[str, Depends(get_current_active_user)]):
    first_name_display = current_user.first_name.title()
    return templates.TemplateResponse("/pages/profile.html", {"request": request, "first_name_display": first_name_display, "user": current_user})

@router.get("/dashboard", response_class=HTMLResponse)
async def user_dashboard(request: Request, current_user: Annotated[str, Depends(get_current_active_user)]):
    first_name_display = current_user.first_name.title()
    img_history = get_user_generated_history(current_user)
    alt_history = []
    for image in img_history:
        alttext = get_image_alt_text(image)
        alt_history.append(alttext)
    
    generated_history = list(zip(img_history, alt_history))
            
    if current_user.role == 'admin':
        users = get_all_users()
        print(users)
        return templates.TemplateResponse("pages/dashboard.html", {"request": request, 
                                                                   "user": current_user, 
                                                                   "first_name_display": first_name_display, 
                                                                   "role": current_user.role, 
                                                                   "users": users, 
                                                                   "generation_history": generated_history})

    return templates.TemplateResponse("pages/dashboard.html", {"request": request, 
                                                               "user": current_user, 
                                                               "first_name_display": first_name_display,  
                                                               "role": current_user.role, 
                                                               "generation_history": generated_history})
        
@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("/pages/login.html", {"request": request})

@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("/pages/signup.html", {"request": request})

@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("token")
    return response

@router.post("/login", response_class=HTMLResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    # login_for_access_token -> authenticate_user -> get_user -> verify_password -> END
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # create_access_token -> END
    access_token = create_access_token(
        data = {"sub": user.username}, 
        expires_delta = access_token_expires
    )

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="token", value=f"Bearer {access_token}", httponly=True)

    return response

@router.post("/signup", response_class=HTMLResponse)
async def signup_user(username: Annotated[str, Form()],
                      first_name: Annotated[str, Form()],
                      last_name: Annotated[str, Form()], 
                      email: Annotated[str, Form()], 
                      plain_password: Annotated[str, Form()],
                      session: SessionDep):
    print(f"SIGNUP SESSION: {session}")

    verify_username(username)
    verify_first_name(first_name)
    verify_last_name(last_name)
    verify_email(email)
    verify_password_strength(plain_password)

    hashed_password = get_password_hash(plain_password)
    
    user = UserCreate(
        username = username,
        first_name = first_name,
        last_name = last_name,
        email = email,
        hashed_password = hashed_password,
        disabled = False,
    )
    user = await create_user(user, session)
    print("USER DONE SIGNUP")
    response = RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
    return response 


@router.post("/profile/update-username", response_class=HTMLResponse)
async def update_username(
    username: Annotated[str, Form()],
    token: Annotated[str, Cookie(...)],
):
    verify_username(username)

    user = UserUpdate(
        username = username
    )
    
    curr_user = await get_current_active_user(await get_current_user(token = token, allow = None))
    user = await update_user_username(user, curr_user)
    
    response = RedirectResponse("/auth/profile", status_code=status.HTTP_302_FOUND)
    return response

@router.post("/profile/update-profile", response_class=HTMLResponse)
async def update_user(
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()], 
    email: Annotated[str, Form()], 
    token: Annotated[str, Cookie(...)],
    disabled: Annotated[bool, Form()] = 0,
):  
    verify_first_name(first_name)
    verify_last_name(last_name)
    verify_email(email)
    
    user = UserUpdate(
        first_name = first_name,
        last_name = last_name,
        email = email,
        disabled = disabled,
    )
    curr_user = await get_current_active_user(await get_current_user(token = token, allow = None))
    user = await update_user_profile(user, curr_user)

    response = RedirectResponse("/auth/profile", status_code=status.HTTP_302_FOUND)
    return response

@router.post("/profile/change-password", response_class=HTMLResponse)
async def change_password(
    curr_password: Annotated[str, Form()],
    change_password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    token: Annotated[str, Cookie(...)]
):
    curr_user = await get_current_active_user(await get_current_user(token = token, allow = None))

    verify_password_strength(change_password)

    if not verify_password(curr_password, curr_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid curent password",
        )
    
    if verify_password(change_password, curr_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be the same as old password",
        )

    if change_password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password does not match",
        )
    
    hashed_password = get_password_hash(change_password)
    user = UserPasswordUpdate(
        hashed_password=hashed_password
    )

    user = await change_user_password(user, curr_user)

    response = RedirectResponse("/auth/profile", status_code=status.HTTP_302_FOUND)
    return response

@router.get("/experiment", response_model=Page)
async def read_users(session: SessionDep, pagination: PaginationInput):
    return await paginate(select(User), session, pagination)