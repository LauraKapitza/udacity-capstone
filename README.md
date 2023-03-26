# Dancing Queen Studio Project

## Introduction

This project is a digital dancing school where dance teachers can create and manage dance courses. 
Students can register to a course they like.

The app is available under this [render link](https://dacing-queen-studio.onrender.com).

## Getting started

### Dependency installations

1. Install python and pip:
 - Python 3.8: follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).
 - pip 21.3.1: when installing python, pip will be automatically installed as well.

2. Create a virtual Environment
It is recommended to work within a virtual environment whenever using python. 
Follow these [instructions](https://docs.python.org/3/library/venv.html) of the python docs to create a virtual environment for this project.

3. Install dependencies:
Once you have created and run your virtual environment, run the following command:

```
pip install -r requirements.txt
```
This will install all required packages for this project.


### Run the server locally

1. Set up the database
```
createdb -U postgres dance
```

2. Run migrations:
```
flask db upgrade
```

3. Run the server:

```
export FLASK_APP=app.py
flask run --reload
```

### Run tests

The project contain a [postman collection](udacity-capstone-dancestudio.postman_collection.json) which can be uploaded on Postman.

Furthermore, it also contains [test files](tests) that can be executed with the following command:
```
./run_tests.sh
```


## Documentation index

Roles: [link](documentation/roles.md)

Classes: [link](documentation/classes.md)

Teachers: [link](documentation/teachers.md)

Students: [link](documentation/students.md)

Dance Types: [link](documentation/dance_types.md)

API Errors: [link](documentation/api_errors.md)


## Models

![alt text](.github/dancing-queens-studio.drawio.png)



## Deployment

Render.com is linked to this Github repository, whenever a new commit is pushed on 
master, it triggers a new deployment using the last commit.