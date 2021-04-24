from fastapi import FastAPI
from .database import add_data, get_student

app = FastAPI()  # API object


@app.get("/")
def check_app():  # checks that API works
    add_data()
    return {"message": "It works fine :)"}


@app.get("/grades/{fullname}")
def get_gpa(fullname: str):
    gpa = get_student(name=fullname)
    if gpa is None:
        return {"No such student"}
    else:
        return({
            "fullname": fullname,
            "gpa": float(gpa)
        })