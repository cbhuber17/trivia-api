import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # -----------------------------------------------------------------------------------------------------------

    def test_get_request_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_get_request_all_categories_404(self):
        res = self.client().get('/categorie')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_post_request_all_categories_405(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_get_request_pagination_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_get_request_pagination_questions_404(self):
        res = self.client().get('/question')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_post_request_pagination_questions_405(self):
        res = self.client().patch('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    # This can only be done once!  Then the db needs to be reloaded
    # (per the instructions in the backend readme.md file)
    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question'], 2)
        self.assertTrue(len(data))

    def test_delete_question_405(self):
        res = self.client().get('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_delete_question_404(self):
        res = self.client().delete('/questions/100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    # This can only be done once!  Then the db needs to be reloaded
    # (per the instructions in the backend readme.md file)
    def test_add_question_to_db(self):
        res = self.client().post('/questions',
                                 json={'question': 'question1', 'answer': 'answer1', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_add_question_to_db_405(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_add_question_to_db_400(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_search_questions(self):
        res = self.client().post('/search', json={'searchTerm': 'Title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_search_questions_400(self):
        res = self.client().post('/search', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_search_questions_405(self):
        res = self.client().get('/search', json={'searchTerm': 'Title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_get_questions_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_get_questions_category_405(self):
        res = self.client().post('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_get_questions_category_400(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_play_trivia_game(self):
        res = self.client().post(
            '/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 1}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_play_trivia_game_405(self):
        res = self.client().get(
            '/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 1}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_play_trivia_game_400(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
