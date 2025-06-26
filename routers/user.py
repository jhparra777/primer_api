from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.security import HTTPBearer
from user_jwt import crearTokenJWT, validateTokenJWT
from db.database import Session, engine, Base
from models.movie import Movie as ModelMovie  
from fastapi.encoders import jsonable_encoder  
from fastapi import APIRouter

routerLogin = APIRouter()

class User(BaseModel):
    email : str
    password: str
    
@routerLogin.post("/login", tags=["Autenticacion"])
def login(user: User):
    if user.email == "jesus@correo.com" and user.password == "123456": 
        token: str = crearTokenJWT(user.dict())
        print(token)
        return JSONResponse(content={"token": token})
