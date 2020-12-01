import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # -----------------------------------------------------------------------------------------------------------

    def pagination(items):
        ''' Helper function: Returns the first 10 elements in a list. '''

        # Pagination
        # Get the value of key 'page' from the request.args object
        # The second argument 1 is default if 'page' does not exist
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start+QUESTIONS_PER_PAGE

        return items[start:end]

    # -----------------------------------------------------------------------------------------------------------

    # After a request is received, run this after_request method
    @app.after_request
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/categories')
    def get_reqest_all_categories():
        ''' Endpoint to handle GET requests for all available categories. '''

        if request.method != 'GET':
            abort(405)

        all_categories_from_db = Category.query.all()
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

        return jsonify(result)

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/questions')
    def get_request_pagination_questions():
        ''' Endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint returns a list of questions,
        number of total questions, current category, categories. '''

        if request.method != 'GET':
            abort(405)

        result = {}

        # Get the questions from the db
        all_questions_from_db = Question.query.all()
        all_questions = []

        # Throw an error if there are no questions in the db
        if len(all_questions_from_db) == 0:
            abort(404)

        # Format the question objects for frontend\src\components\QuestionView.js
        for question_from_db in all_questions_from_db:
            all_questions.append(question_from_db.format())

        result['questions'] = pagination(all_questions)
        result['total_questions'] = len(all_questions)

        # Get the categories from the db
        all_categories_from_db = Category.query.all()
        all_categories = {}

        # Throw an error if there are no categories in the db
        if len(all_categories_from_db) == 0:
            abort(404)

        # Extract categories from backend db and put in format for front end
        for category_from_db in all_categories_from_db:
            all_categories[category_from_db.id] = category_from_db.type

        # Send API data the format the front end requires in frontend\src\components\QuestionView.js
        result['current_category'] = None
        result['categories'] = all_categories
        result['success'] = True

        return jsonify(result)

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        ''' Endpoint to DELETE question using a question ID. '''

        if request.method != 'DELETE':
            abort(405)

        error = False
        question = Question.query.get(id)

        try:
            question.delete()
        except:
            error = True
            question.cancel()
            print(sys.exc_info())
        finally:
            question.close()

        if error:
            abort(422)
        else:
            # TODO: also add key value pair (for completeness): 'deleted_question': id
            return jsonify({'success': True})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/questions', methods=['POST'])
    def add_question_to_db():
        ''' Endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score. '''

        if request.method != 'POST':
            abort(405)

        error = False
        form_data = request.get_json()

        if not form_data['question'] or not form_data['answer']:
            abort(400)

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
            question.cancel()
            print(sys.exc_info())

        finally:
            question.close()

        if error:
            # Throw a 422
            abort(422)

        else:
            # TODO: also add key value pair: 'created_question_id': question.id
            return jsonify({'success': True})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/search', methods=['POST'])
    def search_questions():
        ''' Endpoint to get questions based on a search term.
        It returns any questions for whom the search term
        is a substring of the question. '''

        if not request.method == 'POST':
            abort(405)

        data = request.get_json()
        search_term = data.get('searchTerm')

        if not search_term:
            abort(400)

        # Case insensitive search in the db using ilike
        question_results = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))).all()

        returned_results = []
        returned_categories = []

        for question in question_results:
            returned_results.append(question.format())
            returned_categories.append(question.format()['category'])

        # Send API data the format the front end requires in frontend\src\components\QuestionView.js
        response = {}
        response['total_questions'] = len(returned_results)
        response['questions'] = pagination(returned_results)
        response['current_category'] = returned_categories
        response['success'] = True

        return jsonify(response)

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/categories/<category_id>/questions')
    def get_questions_category(category_id):
        ''' Endpoint to get questions based on category. '''

        if request.method != 'GET':
            abort(405)

        questions_by_category = Question.query.filter(
            Question.category == category_id).all()

        response = {}
        response['questions'] = []

        for question in questions_by_category:
            response['questions'].append(question.format())

        # Send API data the format the front end requires in frontend\src\components\QuestionView.js
        response['questions'] = pagination(response['questions'])
        response['success'] = True
        response['total_questions'] = len(response['questions'])
        response['current_category'] = category_id

        return jsonify(response)

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/quizzes', methods=['POST'])
    def play_trivia_game():
        ''' Endpoint to get questions to play the quiz.
        This endpoint takes a category and previous question parameters
        (from the front end) and return a random questions within the given category,
        if provided, and that is not one of the previous questions. '''

        if request.method != 'POST':
            abort(405)

        data = request.get_json()

        if not data:
            abort(400)

        previous_questions_id = data['previous_questions']
        category_id = data['quiz_category']['id']

        if category_id == 0:
            questions_by_category = Question.query.all()
        else:
            questions_by_category = Question.query.filter(
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

        # Send API data the format the front end requires in frontend\src\components\QuizView.js
        return jsonify({'success': True, 'question': random_question})

    # -----------------------------------------------------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'error': 400, 'message': 'Bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404, 'message': 'Not found'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'success': False, 'error': 405, 'message': 'Method not allowed'}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False, 'error': 422, 'message': 'Not processable'}), 422

    # -----------------------------------------------------------------------------------------------------------

    return app
