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

        # Extract from backend db and put in format for front end
        # Format: {int id: string category} (for each category)
        # TODO: Use Category.format already built in models
        for category_from_db in all_categories_from_db:
            all_categories[int(category_from_db.id)] = category_from_db.type

        return jsonify(all_categories)

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

        # TOOD: Use Question.format in models (?)
        all_questions_from_db = db.session.query(Question).all()
        all_questions = []

        for question_from_db in all_questions_from_db:
            all_questions.append(question_from_db.question)

        result['questions'] = all_questions
        result['num questions'] = len(all_questions)

        # TODO: Use built in Category.format in models
        all_categories_from_db = db.session.query(Category).all()
        all_categories = []
        for category_from_db in all_categories_from_db:
            all_categories.append(category_from_db.type)

        result['current category'] = all_categories[0]
        result['categories'] = all_categories

        return jsonify(result)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):

        # TODO: Activate code when ready to test delete functionality
        # error = False
        # question = Question.query.get(id)

        # try:
        #     db.session.delete(question)
        #     db.session.commit()
        # except:
        #     error = True
        #     db.session.rollback()
        #     print(sys.exc_info())
        # finally:
        #     db.session.close()

        # if error:
        #     flash('An error occurred attempting to delete the question.')
        # else:
        #     flash('Question was deleted.')

        # TODO: Decide if page should be redirected or just return a message
        # return redirect(url_for('pages/home.html'))

        return jsonify({'code': 'deleted'})

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question_to_db():

        error = False

        # TODO: Get the data from the front end forms
        # try:
        #     # question = Question(
        #     #     queston=form.x
        #     #     answer=form.x
        #     #     category=form.x
        #     #     difficulty=form.x
        #     # )

        #     db.session.add(question)
        #     db.session.commit()
        # except:
        #     error = True
        #     db.session.rollback()
        #     print(sys.exc_info())

        # finally:
        #     db.session.close()

        # if error:
        #     flash('ERROR: Question {} could not be added to the db.'.format(form.x))

        #     # TODO: What to do when failing adding to the db
        #     # return render_template('forms/new_venue.html', form=form)

        # else:
        #     flash('SUCCESS! Question {} was added to the db!'.format(form.x))

        #     # TODO: What to do after adding a question
        #     # return render_template('pages/home.html')

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/search', methods=['POST'])
    def search_questions():
        search_term = request.form.get('search_term', '')

        question_results = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))).all()

        returned_results = []

        for question in question_results:
            returned_results.append(question)

        response = {}
        response['num questions'] = len(returned_results)
        response['questions'] = returned_results

        return jsonify(response)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    # TODO: Not sure if category is string or id, currently assuming id
    @app.route('/questions/<category_id>')
    def get_questions_category(category_id):

        questions_by_category = db.session.query(Question).filter(
            Question.category == category_id).all()

        return jsonify({'data': 'ok'})

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
    @app.route('/play/<category_id>/<prev_question_id>', methods=['POST'])
    def play_trivia_game(category_id, prev_question_id):

        # TODO: error handling if question or category doesn't exist

        questions_by_category = db.session.query(Question).filter(
            Question.category == category_id).all()

        questions_to_play = []

        for question in questions_by_category:

            # Don't add previous question to the list
            if prev_question_id == question.id:
                continue

            else:
                questions_to_play.append(question.question)

        random_question = random.choice(questions_to_play)

        return jsonify({'question': random_question})

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    # TODO: Test this after 404 works below
    # def html_code_error(error_code, error_message):
    #     @app.errorhandler(error_code)
    #     def specific_html_error(error):
    #     return jsonify({'success': False, 'error': error_code, 'message': error_message})

    @app.errorhandler(404)
    def not_found(error):  # TODO: what is error?
        return jsonify({'success': False, 'error': 404, 'message': 'Not found'})

    return app
