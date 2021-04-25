from fastapi import FastAPI
from .database import add_data, get_student

app = FastAPI()  # API app
add_data()  # Grabs Data from .csv file

@app.get("/")
def check_app():  # checks that API works

    return {"message": "It works fine :)"}


@app.get("/grades/{fullname}")
def get_gpa(fullname: str):
    """
    Gets GPA by Student's name
    :param fullname: name of the student
    """
    gpa = get_student(name=fullname)
    if gpa is None:  # Student is not found
        return {"No such student"}
    else:  # Student is found
        return({
            "fullname": fullname,
            "gpa": float(gpa)
        })