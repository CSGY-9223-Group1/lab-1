import unittest
from main import app

class PastebinUnitTest(unittest.TestCase):

    # Set up the Flask test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test the home route
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    # get not supported
    def test_register_get_fail1(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 405)
        
    # post with no content fails
    def test_register_post_fail1(self):
        response = self.app.post('/register')
        self.assertEqual(response.status_code, 415)
        
    def test_register_post_valid(self):
        response = self.app.post('/register', json={"id": "ajit1@ajit.com","name": "Ajit S"})
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        print("Response - " + str(response.data))
        
    def test_get_all_notes_without_token(self):
        response = self.app.get('/get_all_notes')
        self.assertEqual(response.status_code, 403) 
        
    def test_add_note_without_token(self):
        response = self.app.post('/add_note')
        self.assertEqual(response.status_code, 403) 
        
    def test_delete_note_without_token(self):
        response = self.app.post('/delete_note')
        self.assertEqual(response.status_code, 403) 

    def test_update_note_without_token(self):
        response = self.app.post('/update_note')
        self.assertEqual(response.status_code, 403) 
        
    def test_get_all_notes_with_invalid_token(self):
        headers = {
            'Content-Type': 'application/json',
            'token': 'invalid_token'
        }
        response = self.app.get('/get_all_notes', headers=headers)
        print("test_get_all_notes_with_invalid_token Response - " + str(response.data))
        self.assertEqual(response.status_code, 403) 
        
    def test_add_note_with_invalid_token(self):
        headers = {
            'Content-Type': 'application/json',
            'token': 'invalid_token'
        }
        response = self.app.get('/add_note', headers=headers)
        print("test_get_all_notes_with_invalid_token Response - " + str(response.data))
        self.assertEqual(response.status_code, 405) 
        
        
    def test_delete_note_with_invalid_token(self):
        headers = {
            'Content-Type': 'application/json',
            'token': 'invalid_token'
        }
        response = self.app.post('/delete_note', headers=headers)
        print("test_get_all_notes_with_invalid_token Response - " + str(response.data))
        self.assertEqual(response.status_code, 403) 

    def test_update_note_with_invalid_token(self):
        headers = {
            'Content-Type': 'application/json',
            'token': 'invalid_token'
        }
        response = self.app.post('/update_note', headers=headers)
        print("test_get_all_notes_with_invalid_token Response - " + str(response.data))
        self.assertEqual(response.status_code, 403) 


if __name__ == '__main__':
    unittest.main()