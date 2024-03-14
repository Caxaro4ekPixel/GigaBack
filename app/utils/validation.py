from pydantic import BaseModel


class LoginUser(BaseModel):
    username: str
    password: str


class RegisterUser(BaseModel):
    username: str
    email: str
    phone: str
    password: str
