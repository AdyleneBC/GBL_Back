from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL de conexión a tu base de datos PostgreSQL
# Formato: "postgresql://usuario:contraseña@host:puerto/nombre_db"
DATABASE_URL = "postgresql://user:password@localhost/gamedb" # ¡Cámbiala por tu URL real!

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Jugador(Base):
    __tablename__ = "jugadores"
    jugador_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    fecha_registro = Column(TIMESTAMP)
    
    # Relaciones
    inventario = relationship("Inventario", back_populates="jugador")
    progreso = relationship("Progreso", back_populates="jugador")

class Inventario(Base):
    __tablename__ = "inventario"
    inventario_id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugadores.jugador_id"), nullable=False)
    objeto_id = Column(Integer, nullable=False) # Simplificado por ahora, podría ser una FK a una tabla de 'Objetos'
    cantidad = Column(Integer)
    
    jugador = relationship("Jugador", back_populates="inventario")

class Mazmorra(Base):
    __tablename__ = "mazmorras"
    mazmorra_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    tipo_medalla = Column(Integer)
    dificultad = Column(Integer)
    orden = Column(Integer, nullable=False)
    
    enemigos = relationship("Enemigo", back_populates="mazmorra")
    progresos = relationship("Progreso", back_populates="mazmorra")

class Enemigo(Base):
    __tablename__ = "enemigos"
    enemigo_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    poder = Column(Integer)
    mazmorra_id = Column(Integer, ForeignKey("mazmorras.mazmorra_id"), nullable=False)
    
    mazmorra = relationship("Mazmorra", back_populates="enemigos")

class Progreso(Base):
    __tablename__ = "progreso"
    progreso_id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugadores.jugador_id"), nullable=False)
    mazmorra_id = Column(Integer, ForeignKey("mazmorras.mazmorra_id"), nullable=False)
    medalla_id = Column(Integer)
    completada = Column(Boolean, default=False)
    fecha_inicio = Column(TIMESTAMP)
    fecha_fin = Column(TIMESTAMP)
    
    jugador = relationship("Jugador", back_populates="progreso")
    mazmorra = relationship("Mazmorra", back_populates="progresos")

# Nota: La tabla 'Posiones' no está directamente relacionada en el diagrama a las otras.
# Se podría relacionar a través de 'Inventario' si 'objeto_id' se refiere a 'posion_id'.
class Posion(Base):
    __tablename__ = "posiones"
    posion_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String)
    descripcion = Column(Text)
    efecto = Column(String)

# Crear las tablas en la base de datos (se ejecuta una sola vez)
def create_tables():
    Base.metadata.create_all(bind=engine)

# Descomenta la siguiente línea y ejecuta este archivo (`python models.py`)
# la primera vez para crear las tablas en tu base de datos de PostgreSQL.
# create_tables()