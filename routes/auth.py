# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth import create_access_token, authenticate_user, get_password_hash, get_current_user
from app.database.mysql_db import get_db
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db=Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    
    # Hashear la contraseña
    hashed_password = get_password_hash(user.password)
    
    # Crear nuevo usuario
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Usuario registrado exitosamente", "username": new_user.username}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}
