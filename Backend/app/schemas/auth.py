from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RegisterResponse(BaseModel):
    message: str
    user_id: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str

class UpdateUser(BaseModel):
    username: str
    email: EmailStr

class ChangePassword(BaseModel):
    current_password: str
    new_password: str