from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """Base para la validación de datos comunes de usuario."""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Esquema para crear un nuevo usuario."""
    password: str

class UserInDB(UserBase):
    """Esquema para usuarios almacenados en la base de datos."""
    id: int
    
    class Config:
        orm_mode = True

class UserOut(UserBase):
    """Esquema para la salida de datos de un usuario."""
    id: int
    
    class Config:
        orm_mode = True
