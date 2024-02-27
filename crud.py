from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc
import models, schemas

def get_users(db:Session):
    db_users = db.query(models.User).all()
    return db_users

def create_user(db:Session,user:schemas.Create_User):
    try:
        db_insert = models.User(username=user.username, useremail=user.useremail, password=user.password)
        db.add(db_insert)
        db.commit()
    except exc.IntegrityError as ec:
        raise HTTPException(status_code=202,detail=f"{ec}")
    else:
        db.refresh(db_insert)

    return db_insert.username


def update_user(db: Session, user_id: int, user: schemas.Create_User):
    data = db.query(models.User).filter(models.User.id == user_id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"User id:{user_id} data was not found")
    elif data:
        for key, value in user.dict().items():
            setattr(data, key, value)
        db.commit()

    return data

def delete_user(db:Session,user_id:int):
    data = db.query(models.User).filter(models.User.id==user_id).first()
    if data:
        db.query(models.User).filter(models.User.id==user_id).delete()
    else:
        raise HTTPException(status_code=404, detail=f"User id:{user_id} data was not found")
    db.commit()
    
    return {"sucess":f"user id :{user_id} was deleted successfully!"}

def user_by_id(db:Session,user_id:int):
    data = db.query(models.User).filter(models.User.id==user_id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"User id:{user_id} data was not found")
    return data
