from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, hashing, models, token

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create(request: schemas.User, db: Session):
    hashed_password = hashing.Hash.bcrypt(request.password)
    user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_one(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': 'Data Not Found',
            'data': None,
            'errors': None
        })

    return user


def login(request: schemas.Login, db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Email/Password')

    if not hashing.Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Email/Password')

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        # data={"sub": user.email}, expires_delta=access_token_expires
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
