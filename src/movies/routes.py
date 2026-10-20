from fastapi import APIRouter, HTTPException, status

from .schema import Movie, MovieCreateModel, MovieUpdateModel
from .service import MovieService


movie_router = APIRouter()
movie_service = MovieService()


@movie_router.get("/", response_model=list[Movie])
async def get_all_movies():
    return movie_service.get_all_movies()


@movie_router.get("/{movie_id}", response_model=Movie)
async def get_movie(movie_id: int):
    movie = movie_service.get_movie(movie_id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )
    return movie


@movie_router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movie(movie_data: MovieCreateModel):
    return movie_service.create_movie(movie_data)


@movie_router.patch("/{movie_id}", response_model=Movie)
async def update_movie(movie_id: int, update_data: MovieUpdateModel):
    movie = movie_service.update_movie(movie_id, update_data)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )
    return movie


@movie_router.delete("/{movie_id}", status_code=status.HTTP_200_OK)
async def delete_movie(movie_id: int):
    movie = movie_service.delete_movie(movie_id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )
    return {"message": "Movie deleted", "movie": movie}
