from django.test import TestCase

import json, requests

class PostTests(TestCase):
    user_id = None
    
        
    def testcreatePost(self):
        url = "http://127.0.0.1:8000/social/post"

        payload1 = json.dumps({
        "title": "Title 4",
        "description": "Description 4"
        })
        
        payload2 = json.dumps({
        "description": "Description 4"
        })
        
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub3ciOiIyMDIyLTExLTIyIDEzOjQyOjI5LjY1NTkzMyIsInVzZXJfaWQiOjN9.bNEov6ayFXE25geGI2W7s4WCAn92h0bOYh5E3Wqb1Y4',
        'Content-Type': 'application/json'
        }

        response1 = requests.request("POST", url, headers=headers, data=payload1)
        response2 = requests.request("POST", url, headers=headers, data=payload2)
        
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 400)
        
        return json.loads(response1.text)['user_id']
        
    def test_like_post(self):
        user_id = self.testcreatePost()
        url = f"http://127.0.0.1:8000/social/post/like/{user_id}"
        url2 = f"http://127.0.0.1:8000/social/post/like/{user_id}22"

        payload={}
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub3ciOiIyMDIyLTExLTIyIDEzOjQyOjI5LjY1NTkzMyIsInVzZXJfaWQiOjN9.bNEov6ayFXE25geGI2W7s4WCAn92h0bOYh5E3Wqb1Y4',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response2 = requests.request("POST", url2, headers=headers, data=payload)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 500)
        
    def test_unlike_post(self):
        user_id = self.testcreatePost()
        url = f"http://127.0.0.1:8000/social/post/unlike/{user_id}"
        url2 = f"http://127.0.0.1:8000/social/post/unlike/{user_id}22"
        
        payload={}
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub3ciOiIyMDIyLTExLTIyIDEzOjQyOjI5LjY1NTkzMyIsInVzZXJfaWQiOjN9.bNEov6ayFXE25geGI2W7s4WCAn92h0bOYh5E3Wqb1Y4',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response2 = requests.request("POST", url2, headers=headers, data=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 500)