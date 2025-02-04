from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User).where(User.id is not None)).all()
    return users


@router.get('/user_id')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalars(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    return user


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], user: CreateUser):
    db.execute(insert(User).values(username=user.username,
                                   firstname=user.firstname,
                                   lastname=user.lastname,
                                   age=user.age,
                                   slug=slugify(user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, user: UpdateUser):
    existing_user = db.execute(select(User).where(User.id == user_id)).one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.execute(update(User).where(User.id == user_id).values(firstname=user.firstname,
                                                             lastname=user.lastname,
                                                             age=user.age))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    existing_user = db.execute(select(User).where(User.id == user_id)).one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful!'
    }
