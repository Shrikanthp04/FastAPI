from fastapi import FastAPI,Depends,HTTPException
import models, schemas, crud
from database import Base, get_db,engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/user/")
async def creates_user(user : schemas.Create_User,db: Session=Depends(get_db)):
    username = crud.create_user(db=db,user=user)
    return f"user {username} was created successfully!"

@app.get("/users/", response_model=list[schemas.User])
async def get_all_users(db:Session=Depends(get_db)):
    data = crud.get_users(db=db)
    if len(data)==0:
        raise HTTPException(status_code=404, detail=f"users data was not found!!!")
    return data

@app.get("/user/{id}")
async def get_user_by_id(id:int, db: Session=Depends(get_db)):
    return crud.user_by_id(db=db,user_id=id)

@app.put("/user/{id}",response_model=schemas.User)
async def update_user(id:int,user:schemas.Create_User,db: Session=Depends(get_db)):
    user = crud.update_user(db=db,user_id=id,user=user)
    return user

@app.delete("/user/{id}")
async def deletes_user(id:int, db: Session=Depends(get_db)):
    return crud.delete_user(db=db,user_id=id)

