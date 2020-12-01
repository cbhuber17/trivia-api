# Full Stack Trivia API Backend

## Getting Started

Note: The instructions below are for a Windows 10 platform.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs.](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Python 3.8 mod

Go into backend\env\Lib\site-packages\sqlalchemy\util\compat.py and follow the instructions here: https://knowledge.udacity.com/questions/132762#132817
Also: pip install --upgrade Werkzeug

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

For Windows 10, this means going into the backend\env\Scripts folder and running ```activate.bat``` via command prompt.  Now this command prompt has (env) in it and is the virtual environment for this project, only containing the dependencies required for it (i.e. those from requirements.txt).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```
createdb -U postgres trivia
psql -U postgres trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 405 and 422. 

## API Documentation

### GET /categories

- Fetches a dictionary of all categories.
- Request Arguments: none
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs:
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
### GET /questions?page=page_number

- Fetches a dictionary (paginated) of questions from the categories
- Request Arguments (optional): page_number:int
- Returns: A dictionary containing the complete list of categories and the paginated questions list:
 ``` {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

### DELETE /questions/id
- Deletes a question from the database with a given id
- Request Arguments: id:int
- Returns: A dictionary containing the deleted ID number:
```
{
  "deleted_question": "2", 
  "success": true
}
```

### POST /questions
- Adds an additional question to the database
- Request Arguments: dictionary: {question: str, answer: str, category: str, difficulty: int}
- Returns: A dictionary indicating the question was successfully added:
```
{
  "success": true
}
```

### POST /search?page=page_number
- Returns questions that matches the search string (case insensitive) and is paginated
- Request Arguments: dictionary: {searchTerm: str}, (optional): page_number:int
- Returns: A dictionary of the search results:
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### GET /categories/category_id/questions

- Returns a dictionary of questions for the input category id
- Request Arguments: category_id:int
- Returns: A dictionary of the questions grouped by the category:
```
{
  "current_category": "1", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

### POST /quizzes
- Captures a single random question within a specified category. Questions that were already played are not used.
- Request Arguments: {previous_questions: list, quiz_category: {id: int, type: str}}
- Returns: A dictionary of the question to be played:
```
{
  "question": {
    "answer": "Blood", 
    "category": 1, 
    "difficulty": 4, 
    "id": 22, 
    "question": "Hematology is a branch of medicine involving the study of what?"
  }, 
  "success": true
}
```

## Testing
To run the tests, open a command window in the ```backend``` directory and run the following:
```
dropdb -U postgres trivia_test
createdb -U postgres trivia_test
psql -U postgres  trivia_test < trivia.psql
python test_flaskr.py
```