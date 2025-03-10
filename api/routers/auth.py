from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from ..utils.auth import (
    get_password_hash,
    create_access_token,
    verify_password,
    get_current_user,
)
from ..models.user import User
from ..utils.database import SessionLocal

router = APIRouter()

@router.post("/register")
def register(email: str, password: str):
    db = SessionLocal()
    
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear un nuevo usuario
    hashed_password = get_password_hash(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"email": db_user.email, "id": db_user.id}  # Devolver el email y el ID del usuario

@router.post("/token")
def login(email: str, password: str):
    db = SessionLocal()
    
    # Buscar al usuario por email
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Crear un token JWT que incluya el user_id como "sub"
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30))
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    # Devolver la información del usuario autenticado
    return {"email": current_user.email, "id": current_user.id}
