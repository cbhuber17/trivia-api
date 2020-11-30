import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, db, Question, Category

# TODO: Perhaps no need to import db (db.session cmds), use the functions in the classes in models.py

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

    # Any origin can access if api is in the path
    # TODO: Not sure this is needed yet
    # CORS(app, resources={r'*/api/*': {'origins': '*'}})

    # After a request is received, run this after_request method
    @app.after_request
    def after_request(response):

        # Return the headers as response - allow Content-Type and Auth and all methods
        # TODO: double check PUT is not needed, or some other method is not used
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    # Basic test rendering simple text
    # TODO remove.
    @app.route('/')
    def index():
        return jsonify({'msg': 'hello!'})

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    # Get all of the categories from the db and transform them to the API
    @app.route('/categories')
    def get_reqest_all_categories():

        all_categories_from_db = db.session.query(Category).all()
        all_categories = {}

        # Throw an error if there are no categories in the db
        if len(all_categories_from_db) == 0:
            abort(404)

        # Extract categories from backend db and put in format for front end
        for category_from_db in all_categories_from_db:
            all_categories[category_from_db.id] = category_from_db.type

        # Send API data the format the front end requires in frontend\src\components\FormView.js
        result = {}
        result['categories'] = all_categories
        result['success'] = True

        # TODO: This may not be needed as I don't see any references/uses in the front end
        # result['total_categories'] = len(all_categories)

        return jsonify(result)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_request_pagination_questions():

        result = {}

        # Get the questions from the db
        all_questions_from_db = db.session.query(Question).all()
        all_questions = []

        # Throw an error if there are no questions in the db
        if len(all_questions_from_db) == 0:
            abort(404)

        # Format the question objects for frontend\src\components\QuestionView.js
        for question_from_db in all_questions_from_db:
            all_questions.append(question_from_db.format())

        # Pagination
        # Get the value of key 'page' from the request.args object
        # The second argument 1 is default if 'page' does not exist
        # TODO: make into function?
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start+QUESTIONS_PER_PAGE

        result['questions'] = all_questions[start:end]
        result['total_questions'] = len(all_questions)

        # Get the categories from the db
        all_categories_from_db = db.session.query(Category).all()
        all_categories = {}

        # Throw an error if there are no categories in the db
        if len(all_categories_from_db) == 0:
            abort(404)

        # Extract categories from backend db and put in format for front end
        for category_from_db in all_categories_from_db:
            all_categories[category_from_db.id] = category_from_db.type

        result['current_category'] = None
        result['categories'] = all_categories

        result['success'] = True

        return jsonify(result)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @ app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):

        error = False
        question = Question.query.get(id)

        try:
            db.session.delete(question)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            abort(422)
        else:
            # TODO: also add key value pair: 'deleted_question': id
            return jsonify({'success': True})

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @ app.route('/questions', methods=['POST'])
    def add_question_to_db():

        error = False
        form_data = request.get_json()

        try:
            question = Question(
                question=form_data['question'],
                answer=form_data['answer'],
                category=form_data['category'],
                difficulty=int(form_data['difficulty'])
            )

            question.insert()

        except:
            error = True

            # TODO: Put a rollback function in the models
            db.session.rollback()
            print(sys.exc_info())

        finally:
            # TODO: need to close session?
            db.session.close()

        if error:
            # Throw a 422
            abort(422)

        else:
            # TODO: also add key value pair: 'created_question': question.id
            return jsonify({'success': True})

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @ app.route('/search', methods=['POST'])
    def search_questions():

        # TODO: Check method in all functions
        # if not request.method == 'POST':
        # abort(405)

        data = request.get_json()
        search_term = data.get('searchTerm')

        # TODO: Do this in other calls when getting data from the front end
        # if not search_term:
        #     abort(422)

        question_results = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))).all()

        returned_results = []
        returned_categories = []

        for question in question_results:
            returned_results.append(question.format())
            returned_categories.append(question.format()['category'])

        # Pagination
        # Get the value of key 'page' from the request.args object
        # The second argument 1 is default if 'page' does not exist
        # TODO: make into function?
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start+QUESTIONS_PER_PAGE

        response = {}
        response['total_questions'] = len(returned_results)
        response['questions'] = returned_results[start:end]
        response['current_category'] = returned_categories
        response['success'] = True

        return jsonify(response)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @ app.route('/categories/<category_id>/questions')
    def get_questions_category(category_id):

        questions_by_category = db.session.query(Question).filter(
            Question.category == category_id).all()

        response = {}
        response['questions'] = []

        for question in questions_by_category:
            response['questions'].append(question.format())

        # Pagination
        # Get the value of key 'page' from the request.args object
        # The second argument 1 is default if 'page' does not exist
        # TODO: make into function?
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start+QUESTIONS_PER_PAGE

        response['questions'] = response['questions'][start:end]
        response['success'] = True
        response['total_questions'] = len(response['questions'])
        response['current_category'] = category_id

        return jsonify(response)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @ app.route('/quizzes', methods=['POST'])
    def play_trivia_game():

        data = request.get_json()
        previous_questions_id = data['previous_questions']
        category_id = data['quiz_category']['id']

        # TODO: error handling if question or category doesn't exist

        if category_id == 0:
            questions_by_category = Question.query.all()
        else:

            # TODO: Not query by db.session
            questions_by_category = db.session.query(Question).filter(
                Question.category == category_id).all()

        questions_to_play = []

        for question in questions_by_category:

            # Don't add previous questions to the list to play
            if question.id in previous_questions_id:
                continue

            questions_to_play.append(question)

        if len(questions_to_play) > 0:
            random_question = random.choice(questions_to_play).format()
        else:
            random_question = None

        return jsonify({'success': True, 'question': random_question})

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @ app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404, 'message': 'Not found'}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False, 'error': 422, 'message': 'Not processable'}), 422

    return app
