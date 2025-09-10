# Prueba de funcionamiento
from fastapi import FastAPI

app = FastAPI(title="No sé qué es esto")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al backend de nuestro Videojuego Group By Legends!"}