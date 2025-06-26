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

routerMovie = APIRouter()

class BearerJWT(HTTPBearer):
    async  def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateTokenJWT(auth.credentials)
        if data['email'] != 'jesus@correo.com':
            raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este recurso")

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Titulo de la pelicula",min_length=5, max_length=60)
    overview: str = Field(default="Descripcion de la pelicula",min_length=15, max_length=100)
    year: int = Field(default=2023)
    rating: float = Field(ge=0, le=10)
    category: str = Field(default="Categoria de la pelicula", min_length=5, max_length=20)

@routerMovie.get("/movies", tags=["Movies"], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"mensaje": "No encontramos la pelicula en la BD"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(data),status_code=200)
    
@routerMovie.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str = Query(default="Aventura", min_length=5, max_length=20)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    if not data:
        return JSONResponse(content={"mensaje": "No encontramos categorias en la BD"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(data), status_code=200)

# Eliminamos los argumentos de la función, ya que no son necesarios
@routerMovie.post("/movies/", tags=["Movies"], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    print(movie)
    return JSONResponse(content={'message':'Ya se ha creado la pelicula correctamente'})
                        

@routerMovie.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"mensaje": "No encontramos la pelicula en la BD"}, status_code=404)
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(content=jsonable_encoder(data), status_code=200)

@routerMovie.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"mensaje": "No encontramos la pelicula en la BD"}, status_code=404)
    print(movies)
    db.delete(data)
    db.commit()
    return JSONResponse(content={"mensaje": "Se ha liminado  la pelicula en la BD", "data": jsonable_encoder(data)}, status_code=404)