from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User


class TestActivityView(TestCase):
    def setUp(self):
        self.student1_data = {
            "username": "student1",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False
        }

        self.student1_login_data = {
            "username": "student1",
            "password": "1234",
        }

        self.student1_data = {
            "username": "student1",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False
        }

    def test_create_activities_student(self):
        client = APIClient()
        client.post('/api/accounts/', self.student1_data, format='json')

        token = client.post(
            '/api/login/', self.student1_login_data).json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 1}

        response = client.post('/api/activities/', activity_data)
        activity = response.json()

        self.assertTrue(response.status_code, 201)
        self.assertTrue(
            activity, {'repo': 'test repo', 'user_id': 1, id: 1, 'grade': None})

    def test_get_activities_student(self):
        client = APIClient()
        client.post('/api/accounts/', self.student1_data, format='json')

        token = client.post(
            '/api/login/', self.student1_login_data).json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 1}

        activity = client.post('/api/activities/', activity_data).json()
        activity = client.post('/api/activities/', activity_data).json()

        self.assertTrue(
            activity, {'repo': 'test repo', 'user_id': 1, 'id': 1, 'grade': None})

        self.assertTrue(
            activity, {'repo': 'test repo', 'user_id': 1, id: 2, 'grade': None})

        activity_list = self.client.get('/api/activities/').json()

        self.assertTrue(activity_list, [{'repo': 'test repo', 'user_id': 1, 'id': 1, 'grade': None}, {
                        'repo': 'test repo', 'user_id': 1, 'id': 2, 'grade': None}])
