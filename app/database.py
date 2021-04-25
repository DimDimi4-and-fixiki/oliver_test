from sqlalchemy import create_engine, Table, MetaData, Column, String, Integer, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from .data_handler import DataHandler
import sqlalchemy

# Url of the Postgres DB:
DATABASE_URL = 'postgresql+psycopg2://user:password@db_con/oliver'
data_handler = DataHandler(path="app/gpa_table.csv")
metadata = MetaData()
data = data_handler.get_data()
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
session = SessionLocal()

# Clears all previous tables:
session.expire_all()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
session.commit()


class Student(Base):
    """
    Students Table definition
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)  # Name column
    mark = Column(String)  # GPA column


def add_data():
    """
    Adds all the rows to the Students Table
    """
    print("ADDED")
    session = SessionLocal()
    for i, row in enumerate(data):  # looping through students
        name, mark = str(row[0]), str(row[-1])
        if name != "nan" and mark != "nan" and get_student(name=name) is None:  # if row is not Null
            try:  # Trying
                new_student = Student(id=i + 1, name=name, mark=mark)
                session.add(new_student)
            except Exception:
                pass
    try:
        session.commit()
    except Exception:
        pass


def get_student(**kwargs):
    """
    Gets Student's GPA by the name
    name: Name of the student
    :return:
    """
    name = str(kwargs.get("name", None))

    # Transforming the name:
    first_name = name.split("-")[0]
    second_name = name.split("-")[-1]
    new_first_name = first_name[0].upper() + first_name[1:]
    new_second_name = second_name[0].upper() + second_name[1:]

    full_name = new_first_name + " " + new_second_name  # Full name of the Student

    #  Performing a query:
    try:
        result = session.query(Student).filter(Student.name == full_name)
    except Exception:
        result = None
    if not list(result):  # No results
        return None
    else:  # Student is found
        for row in result:
            return str(row.mark)