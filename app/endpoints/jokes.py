import os
from random import random
from fastapi import APIRouter
import psycopg2
import requests

from core.schemas.schema import JokeEdit, JokeSave, JokeDelete

# Hay que rellenar los campos de la función connect

router = APIRouter(prefix="/jokes", tags=["jokes"])


url_chuck = "https://api.chucknorris.io/jokes/"
url_dad = "https://icanhazdadjoke.com"

JOKES_PATH = os.path.dirname(os.path.realpath(__file__))+"/../jokes.txt"

database_error_message = "Error: couldn't establish connection to database"


@router.get("/")
async def random_joke():
    if random() < 0.5:
        return requests.get(url_chuck+"random").json()["value"]
    else:
        return requests.get(url_dad, headers={"Accept": "application/json"}).json()["joke"]


@router.get("/{param}")
async def specific_random_joke(param: str):
    if param == "Chuck":
        return requests.get(url_chuck+"random").json()["value"]

    elif param == "Dad":
        return requests.get(url_dad, headers={"Accept": "application/json"}).json()["joke"]

    else:
        return {"message": "Error: invalid value for 'param'"}


def is_joke(number):
    try:
        connection = psycopg2.connect(
            database="", user="", password="", host="", port="")
        cursor = connection.cursor()

        cursor.execute(f"SELECT id_joke FROM joke WHERE id_joke={number}")

        if cursor:
            connection.close()

            return True

        connection.close()

        return False

    except Exception:
        return False


def last_index():
    try:
        connection = psycopg2.connect(
            database="", user="", password="", host="", port="")
        cursor = connection.cursor()

        cursor.execute(f"SELECT MAX(id_joke) FROM joke")

        number = cursor.fetchone()

        connection.close()

        if number is None or number[0] is None:
            return 1

        else:
            return number[0]+1

    except Exception:
        return 1


@router.post("/")
async def save_joke(param: JokeSave):
    if param.joke == "":
        return {"message": "Error: no joke received"}

    else:
        number = last_index()

        try:
            connection = psycopg2.connect(
                database="", user="", password="", host="", port="")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO joke (id_joke, description) VALUES (%s,%s);", (number, param.joke))
            connection.commit()

            connection.close()

        except Exception:
            return {"message": database_error_message}

        return {"message": "Joke saved successfully"}


@router.put("/")
async def update_joke(param: JokeEdit):
    if param.joke == "":
        return {"message": "Error: invalid value for 'joke'"}

    if is_joke(param.number):
        try:
            connection = psycopg2.connect(
                database="", user="", password="", host="", port="")
            cursor = connection.cursor()

            cursor.execute(
                "UPDATE joke SET description=%s WHERE id_joke=%s", (param.joke, param.number))
            connection.commit()

            connection.close()

        except Exception:
            return {"message": database_error_message}

        return {"message": "Joke set successfully"}

    else:
        return {"message": "Joke doesn't already exists"}


@router.delete("/")
async def delete_joke(param: JokeDelete):
    if is_joke(param.number):
        try:
            connection = psycopg2.connect(
                database="", user="", password="", host="", port="")
            cursor = connection.cursor()

            cursor.execute("DELETE FROM joke WHERE id_joke=%s",
                           (param.number,))
            connection.commit()

            connection.close()

        except Exception:
            return {"message": database_error_message}

        return {"message": "Joke deleted successfully"}

    else:
        return {"message": "Joke doesn't already exists"}
