from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.security import HTTPBearer
from user_jwt import crearTokenJWT, validateTokenJWT
from db.database import Session, engine, Base
from models.movie import Movie as ModelMovie  
from fastapi.encoders import jsonable_encoder  
 

app = FastAPI(
    title = "API del agente Hugging Face",
    description= "La siguiente API procseará información con un modelo de IA",
    version = "0.0.1"
)

Base.metadata.create_all(bind=engine)

class BearerJWT(HTTPBearer):
    async  def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateTokenJWT(auth.credentials)
        if data['email'] != 'jesus@correo.com':
            raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este recurso")

class User(BaseModel):
    email : str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Titulo de la pelicula",min_length=5, max_length=60)
    overview: str = Field(default="Descripcion de la pelicula",min_length=15, max_length=100)
    year: int = Field(default=2023)
    rating: float = Field(ge=0, le=10)
    category: str = Field(default="Categoria de la pelicula", min_length=5, max_length=20)

movies = [
    {
        "id": 1,
        "title": "El viaje increíble",
        "overview": "Una historia emocionante sobre un grupo de amigos que emprende un viaje lleno de aventuras y desafíos inesperados.",
        "year": 2022,
        "rating": 8.5,
        "category": "Aventura"
    },
]

@app.post("/login", tags=["Autenticacion"])
def login(user: User):
    if user.email == "jesus@correo.com" and user.password == "123456": 
        token: str = crearTokenJWT(user.dict())
        print(token)
        return JSONResponse(content={"token": token})

@app.get("/", tags=["Inicio"])
def read_root():
    return {"Hello": "World"}

@app.get("/start", tags=["Start"])
def read2_root():
    return HTMLResponse('<h1>Hola, mundo!</h1>')

@app.get("/movies", tags=["Movies"], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"mensaje": "No encontramos la pelicula en la BD"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(data),status_code=200)
    
@app.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str = Query(default="Aventura", min_length=5, max_length=20)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    if not data:
        return JSONResponse(content={"mensaje": "No encontramos categorias en la BD"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(data), status_code=200)

# Eliminamos los argumentos de la función, ya que no son necesarios
@app.post("/movies/", tags=["Movies"], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    print(movies)
    return JSONResponse(content={'message':'Ya se ha creado la pelicula correctamente', 'movie':[movie if isinstance(movie, dict) else movie.dict() for movie in movies]})
                        

@app.put("/movies/{id}", tags=["Movies"])
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

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"mensaje": "No encontramos la pelicula en la BD"}, status_code=404)
    print(movies)
    db.delete(data)
    db.commit()
    return JSONResponse(content={"mensaje": "Se ha liminado  la pelicula en la BD", "data": jsonable_encoder(data)}, status_code=404)