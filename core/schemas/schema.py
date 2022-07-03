from pydantic import BaseModel


class JokeSave(BaseModel):
    joke: str


class JokeEdit(BaseModel):
    number: int
    joke: str


class JokeDelete(BaseModel):
    number: int


class MathsLeastCommonMultiple(BaseModel):
    numbers: list[int]


class MathsPlusOne(BaseModel):
    number: int
