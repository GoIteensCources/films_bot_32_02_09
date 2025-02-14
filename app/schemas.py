from pydantic import BaseModel


class Film(BaseModel):
    title: str
    desc: str
    rating: str
    url: str | None = None
    photo: str
