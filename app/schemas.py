from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Esquemas para Jugadores
class JugadorBase(BaseModel):
    username: str
    email: str

class JugadorCreate(JugadorBase):
    password: str

class Jugador(JugadorBase):
    jugador_id: int
    fecha_registro: datetime

    class Config:
        orm_mode = True

# Esquemas para la autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Esquemas para Progreso
class ProgresoBase(BaseModel):
    mazmorra_id: int

class ProgresoCreate(ProgresoBase):
    pass

class ProgresoUpdate(BaseModel):
    completada: bool

class Progreso(ProgresoBase):
    progreso_id: int
    jugador_id: int
    completada: bool
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

    class Config:
        orm_mode = True