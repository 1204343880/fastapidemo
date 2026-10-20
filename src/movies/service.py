from .movie_data import movies
from .schema import MovieCreateModel, MovieUpdateModel


class MovieService:
    """对内存列表执行 CRUD；此类不接触数据库或 Session。"""

    def get_all_movies(self) -> list[dict]:
        return movies

    def get_movie(self, movie_id: int) -> dict | None:
        for movie in movies:
            if movie["id"] == movie_id:
                return movie
        return None

    def create_movie(self, movie_data: MovieCreateModel) -> dict:
        # 用当前最大 id + 1，避免删除某条记录后 len(movies) 造成 id 重复。
        new_id = max((movie["id"] for movie in movies), default=0) + 1
        new_movie = {"id": new_id, **movie_data.model_dump()}
        movies.append(new_movie)
        return new_movie

    def update_movie(
        self, movie_id: int, update_data: MovieUpdateModel
    ) -> dict | None:
        movie = self.get_movie(movie_id)
        if movie is None:
            return None

        # PATCH 只更新请求 JSON 中实际传来的字段。
        changes = update_data.model_dump(exclude_unset=True)
        movie.update(changes)
        return movie

    def delete_movie(self, movie_id: int) -> dict | None:
        movie = self.get_movie(movie_id)
        if movie is None:
            return None

        movies.remove(movie)
        return movie
