# Movie Web Application

## Description

A web application for COMPSCI-235 assignment2. Developed using Python's Flask framework. Some other libraries/tools used in this project include: Jinja2 for templating, WTForm for secure form post, pytest for testing, editdistance for fuzzy search, etc.

The project used repository design pattern, and currently included a memory repository for data storage, at the mean time, it also implemented a persistent layer for user and review using plain text local files to make sure that a restart of the application wouldn't invalidate all users, and reviews will also be kept after restart.

For testing, this project included unit test, end to end test covered different layers.

## Installation

**Installation via requirements.txt**

```shell
$ cd a3final
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, follow the path of 'File'->'Settings'->'Project:COMPSCI-235-Assignment' to configure the virtual environment: select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. Otherwise, you can also create a new virtual environment from there.

## Execution

**Running the application**

From the *a3final* directory:
````shell
$ flask run
```` 
## Testing

**Running the application**

From the *a3final* directory:
````shell
$ python -m pytest
```` 

Make sure the virtual environment has been selected as the project interpreter

## Configuration

The *a3finals/.env* contains global environment settings include:

- `FLASK_APP`: Entry point of the application
- `FLASK_ENV`: The environment in which to run the application (either `development` or `production`)
- `SECRET_KEY`: Secret key used to encrypt session data
- `TESTING`: Set to False for running the application
- `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library
-'repository': memory or database
