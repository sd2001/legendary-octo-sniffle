from django.test import TestCase

import json, requests

class PostTests(TestCase):
    user_id = None
    def authenticate(self):
        url = "http://127.0.0.1:8000/users/authenticate"

        payload = json.dumps({
        "email": "s2@gmail.com",
        "password": "swarna12345"
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        token = json.loads(response.text)['token']
        return token
        
    def testcreatePost(self):
        token = self.authenticate()
        url = "http://127.0.0.1:8000/social/post"

        payload1 = json.dumps({
        "title": "Title 4",
        "description": "Description 4"
        })
        
        payload2 = json.dumps({
        "description": "Description 4"
        })
        
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub3ciOiIyMDIyLTExLTIzIDA5OjA0OjA1Ljk4MjM0OSIsInVzZXJfaWQiOjN9.rE47cZzqjeDaol1VrRSgS--_qRfoLLvm6WV-5gihRmc',
        'Content-Type': 'application/json'
        }

        response1 = requests.request("POST", url, headers=headers, data=payload1)
        response2 = requests.request("POST", url, headers=headers, data=payload2)
        
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 400)
        
        return json.loads(response1.text)['user_id']
        
    def test_like_post(self):
        token = self.authenticate()
        user_id = self.testcreatePost()
        url = f"http://127.0.0.1:8000/social/post/like/{user_id}"
        url2 = f"http://127.0.0.1:8000/social/post/like/{user_id}22"

        payload={}
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub3ciOiIyMDIyLTExLTE4IDE5OjMxOjU5LjIzMDg3OCIsInVzZXJfaWQiOjJ9.3BjqU8CKyr5KABFTYFQyJdDYOZgN0eCe2XvUEIZxxTs',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response2 = requests.request("POST", url2, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 500)
        
    def test_unlike_post(self):
        token = self.authenticate()
        user_id = self.testcreatePost()
        url = f"http://127.0.0.1:8000/social/post/unlike/{user_id}"
        url2 = f"http://127.0.0.1:8000/social/post/unlike/{user_id}22"
        
        payload={}
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub3ciOiIyMDIyLTExLTE4IDE5OjMxOjU5LjIzMDg3OCIsInVzZXJfaWQiOjJ9.3BjqU8CKyr5KABFTYFQyJdDYOZgN0eCe2XvUEIZxxTs',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response2 = requests.request("POST", url2, headers=headers, data=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 500)