from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    director: str
    production_company: str
    release_date: str
    duration_minutes: int
    language: str


class MovieCreateModel(MovieBase):
    pass


class MovieUpdateModel(BaseModel):
    title: str | None = None
    director: str | None = None
    production_company: str | None = None
    release_date: str | None = None
    duration_minutes: int | None = None
    language: str | None = None


class Movie(MovieBase):
    id: int
