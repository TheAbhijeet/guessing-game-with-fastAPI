import random

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()


class Guess(BaseModel):
    number: int


random_number = random.randint(1, 10)


@app.get("/health", status_code=200)
def health():
    return {"message": "healthy"}


@app.post("/play")
def play(guess: Guess, request: Request, response: Response):
    # note that it's not the best way to do it,
    # A better way would be to save the number in the database and send the encrypted key in cookie
    # Or maybe just encrypt the number while setting it in the cookie
    if 'number_to_guess' not in request.cookies:
        response.set_cookie(key="number_to_guess", value=str(random_number))

    number = int(request.cookies['number_to_guess'])

    if guess.number == number:
        # reset the cookie
        response.set_cookie(key="number_to_guess", value=str(random_number))
        return {"message": "Your guess is right"}

    elif guess.number <= number:
        return {"message": "Your guess is too low"}

    else:
        return {"message": "Your guess is too high"}
