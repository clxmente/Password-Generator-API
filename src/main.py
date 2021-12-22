import random
import string

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

class PasswordNotLongEnough(Exception):
    def __init__(self, length: int) -> None:
        self.length = length

class PasswordTooLong(Exception):
    def __init__(self, length: int) -> None:
        self.length = length

class ExcludedAllSets(Exception):
    pass

def gen_password(length: int, exclude: Optional[str] = None) -> str:
    
    specialChar = "!@#$%^&*()-_"
    bool_special = False
    bool_lower = False
    bool_upper = False
    bool_digits = False
    charsets = [string.ascii_lowercase, string.ascii_uppercase, string.digits, specialChar]
    # Exclude certain character sets if user wants
    if (exclude):
        if ("special" in exclude): 
            charsets.remove(specialChar)
            bool_special = True
        if ("digits" in exclude): 
            charsets.remove(string.digits)
            bool_digits = True
        if ("upper" in exclude): 
            charsets.remove(string.ascii_uppercase)
            bool_upper = True
        if ("lower" in exclude): 
            charsets.remove(string.ascii_lowercase)
            bool_lower = True

        # if all charsets excluded raise error
        if (len(charsets) == 0): raise ExcludedAllSets

    password = []
    for i in range(0, length):
        currsection = random.choice(charsets)
        if (currsection == string.ascii_lowercase): bool_lower=True
        elif (currsection == string.ascii_uppercase): bool_upper=True
        elif (currsection == string.digits): bool_digits=True
        elif (currsection == specialChar): bool_special=True

        currchar = random.choice(currsection)
        password.append(currchar)
    
    if (bool_lower and bool_upper and bool_digits and bool_special):
        # only return the output when all requirements are met
        output = "".join(password)
        return output
    else: return gen_password(length) # try again if all requirements not met

@app.exception_handler(PasswordNotLongEnough)
async def length_handler(request: Request, exc: PasswordNotLongEnough):
    return JSONResponse(
        status_code=400,
        content={
            "length": exc.length,
            "message": "Please choose a password of at least 8 characters!"},
    )

@app.exception_handler(PasswordTooLong)
async def length_too_long(request: Request, exc: PasswordTooLong):
    return JSONResponse(
        status_code=400,
        content={
            "length": exc.length,
            "message": "Please choose a password length under 64 characters ☹️",
        }
    )

@app.exception_handler(ExcludedAllSets)
async def no_sets_selected(request: Request, exc: ExcludedAllSets):
    return JSONResponse(
        status_code=400,
        content={
            "message": "Please select at least one character set."
        }
    )

@app.get("/password")
async def password_endpoint(length: int = 10, exclude: Optional[str] = None):
    if (length < 8):
        raise PasswordNotLongEnough(length)
    elif (length > 64):
        raise PasswordTooLong(length)
    output = gen_password(length, exclude)
    return {
        "length": length,
        "password": output,
    }
