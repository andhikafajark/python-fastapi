from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..database import get_db
from ..repositories import user

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    return user.create(request, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_one(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_one(id, db)
