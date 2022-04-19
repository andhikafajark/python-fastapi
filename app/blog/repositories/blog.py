from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


def get_one(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': 'Data Not Found',
            'data': None,
            'errors': None
        })
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     'message': 'Data Not Found',
        #     'data': None,
        #     'errors': None
        # }

    return blog


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': 'Data Not Found',
            'data': None,
            'errors': None
        })
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     'message': 'Data Not Found',
        #     'data': None,
        #     'errors': None
        # }

    blog.update(request.dict(), synchronize_session=False)
    db.commit()

    return {
        'message': 'Success Update Data',
        'data': None,
        'errors': None
    }


def delete(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': 'Data Not Found',
            'data': None,
            'errors': None
        })
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     'message': 'Data Not Found',
        #     'data': None,
        #     'errors': None
        # }

    blog.delete(synchronize_session=False)
    db.commit()

    return {
        'message': 'Success Delete Data',
        'data': None,
        'errors': None
    }
