from pydantic import BaseModel


class Create_User(BaseModel):
    username : str
    useremail : str
    password :str

class User(Create_User):
    id : int

    class Config():
        orm_mode = True