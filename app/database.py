# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ¡IMPORTANTE! Reemplaza esto con los datos de tu base de datos de Render.
# postgresql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BD
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()