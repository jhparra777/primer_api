from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI(
    title = "API del agente Hugging Face",
    description= "La siguiente API procseará información con un modelo de IA",
    version = "0.0.1"
)

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


@app.get("/", tags=["Inicio"])
def read_root():
    return {"Hello": "World"}

@app.get("/start", tags=["Start"])
def read2_root():
    return HTMLResponse('<h1>Hola, mundo!</h1>')

@app.get("/movies", tags=["Movies"])
def get_movies():
    return movies

@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int):
    for pelicula in movies:
        if pelicula["id"] == id:
            return pelicula
        return {"mensaje": "No encontramos la pelicula en la BD"}
    
@app.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str):
    return category

@app.post("/movies/", tags=["Movies"])
def create_movie(
                id: int = Body(),
                title: str = Body(),
                overview: str = Body(),
                year: int = Body(),
                rating: float = Body(),
                category: str = Body()
                ):
    registro = {
                "id": id,
                "title": title,
                "overview": overview,
                "year": year,
                "rating": rating,
                "category": category
             }
    movies.append(registro)
    print(movies)
    return title

@app.put("/movies/{id}", tags=["Movies"])
def update_movie(
                id: int,
                title: str = Body(),
                overview: str = Body(),
                year: int = Body(),
                rating: float = Body(),
                category: str = Body()
                ):
    for pelicula in movies:
        if pelicula["id"] == id:
            pelicula["title"] = title
            pelicula["overview"] = overview
            pelicula["year"] = year
            pelicula["rating"] = rating
            pelicula["category"] = category
            print(movies)
            return pelicula
        return {"mensaje": "No encontramos la pelicula en la BD"}

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    print(movies)
    for pelicula in movies:
        if pelicula["id"] == id:
            movies.remove(pelicula)
            print(movies)
            return {"mensaje": "Pelicula eliminada correctamente"}
    return {"mensaje": "No encontramos la pelicula en la BD"}