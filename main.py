#from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
#from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional

import uvicorn
# from fastapi.security import HTTPBearer
from user_jwt import crearTokenJWT, validateTokenJWT
from db.database import Session, engine, Base
from models.movie import Movie as ModelMovie  
# from fastapi.encoders import jsonable_encoder  
from routers.movie import routerMovie
from routers.user import routerLogin
import os
 

app = FastAPI(
    title = "API del agente Hugging Face",
    description= "La siguiente API procseará información con un modelo de IA",
    version = "0.0.1"
)

app.include_router(routerMovie, tags=["Movies"])
app.include_router(routerLogin, tags=["Users"])

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Inicio"])
def read_root():  
    return HTMLResponse("<h1>API de Hugging Face</h1><p>Esta es una API para procesar información con un modelo de IA.</p>")

@app.get("/start", tags=["Start"])
def read2_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)