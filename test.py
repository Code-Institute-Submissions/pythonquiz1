# tests/test_basic.py

from run import app
import unittest
import os
import tempfile

class FlaskTestCase(unittest.TestCase):
    
    # Ensure that Flask was set up correctly
    def test_Flask_route(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    # Ensure that Flask index page was set up correctly
    def test_index_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Riddle Game' in response.data)

    # Ensure username behaves correctly with correct response
    def test_quiz_loads_correct_username(self):
        tester = app.test_client(self)
        response = tester.post(
        '/',
        data=dict(username= "{{username}}"),
        follow_redirects=True
        )
        self.assertIn(b'Riddle Game Begin', response.data)
        
        
    # page renders questions
    def test_quiz_loads_questions(self):
        tester = app.test_client(self)
        response = tester.get(
        '/quiz',
        data=dict(question_answer= "{{riddle_index, description}}"),
        follow_redirects=True
        )
        self.assertIn(b'Who was the Roman Goddess of hunting?', response.data)
        
        
        
if __name__ == '__main__':
    unittest.main()