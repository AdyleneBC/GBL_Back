from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Configuración de Autenticación (JWT) ---
SECRET_KEY = "TU_CLAVE_SECRETA_SUPER_SEGURA" # ¡Cámbiala por una clave real y guárdala de forma segura!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_jugador_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# --- Endpoints ---

@app.post("/register/", response_model=schemas.Jugador)
def register(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    db_jugador = crud.get_jugador_by_username(db, username=jugador.username)
    if db_jugador:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    return crud.create_jugador(db=db, jugador=jugador)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_jugador_by_username(db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.Jugador)
async def read_users_me(current_user: schemas.Jugador = Depends(get_current_user)):
    return current_user

@app.get("/progreso/", response_model=List[schemas.Progreso])
def get_user_progress(db: Session = Depends(get_db), current_user: schemas.Jugador = Depends(get_current_user)):
    return crud.get_progreso(db=db, jugador_id=current_user.jugador_id)

@app.put("/progreso/{mazmorra_id}", response_model=schemas.Progreso)
def update_dungeon_progress(
    mazmorra_id: int, 
    progreso: schemas.ProgresoUpdate, 
    db: Session = Depends(get_db), 
    current_user: schemas.Jugador = Depends(get_current_user)
):
    updated_progress = crud.update_progreso_mazmorra(
        db=db,
        jugador_id=current_user.jugador_id,
        mazmorra_id=mazmorra_id,
        progreso=progreso
    )
    if not updated_progress:
        raise HTTPException(status_code=404, detail="Progreso de mazmorra no encontrado")
    return updated_progress