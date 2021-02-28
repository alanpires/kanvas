from django.test import TestCase
from rest_framework.test import APIClient
import ipdb


class TestAccountView(TestCase):
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

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

        self.instructor_data = {
            "username": "instructor",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True
        }

        self.instructor_login_data = {
            "username": "instructor",
            "password": "1234",
        }

    def test_create_and_login_for_student_account(self):
        client = APIClient()
        # create user
        user = client.post(
            '/api/accounts/', self.student1_data, format='json').json()

        self.assertEqual(user, {
            'id': 1,
            "username": "student1",
            "is_superuser": False,
            "is_staff": False
        })

        # login
        response = client.post(
            '/api/login/', self.student1_login_data, format='json').json()

        self.assertIn('token', response.keys())

    def test_create_and_login_for_facilitator_account(self):
        client = APIClient()
        # create user
        user = client.post(
            '/api/accounts/', self.facilitator_data, format='json').json()

        self.assertEqual(user, {
            'id': 1,
            "username": "facilitator",
            "is_superuser": False,
            "is_staff": True
        })

        # login
        response = client.post(
            '/api/login/', self.facilitator_login_data, format='json').json()

        self.assertIn('token', response.keys())

    def test_create_and_login_for_instructor_account(self):
        client = APIClient()
        # create user
        user = client.post(
            '/api/accounts/', self.instructor_data, format='json').json()

        self.assertEqual(user, {
            'id': 1,
            "username": "instructor",
            "is_superuser": True,
            "is_staff": True
        })

        # login
        response = client.post(
            '/api/login/', self.instructor_login_data, format='json').json()

        self.assertIn('token', response.keys())

    def wrong_credentials_do_not_login(self):
        client = APIClient()
        # create user
        response = client.post(
            '/api/accounts/', self.instructor_data, format='json')

        # login
        response = client.post(
            '/api/login/', self.instructor_login_data, format='json').json()

        self.assertIn('token', response.keys())


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

        self.student2_data = {
            "username": "student2",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False
        }

        self.student2_login_data = {
            "username": "student2",
            "password": "1234",
        }

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

    def test_create_activities_student(self):
        client = APIClient()
        activity_data = {'repo': 'test repo', 'user_id': 1}

        # test with no authentication
        response = client.post(
            '/api/activities/', activity_data, format='json')
        self.assertEqual(response.status_code, 401)

        # create user
        client.post('/api/accounts/', self.student1_data, format='json')

        # login
        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create activity
        response = client.post(
            '/api/activities/', activity_data, format='json')
        activity = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            activity, {'repo': 'test repo', 'user_id': 1, 'id': 1, 'grade': None})

    def test_student_cannot_assign_grade(self):
        client = APIClient()
        # student tries to assign grade, but it should not have
        # any effect
        activity_data = {'repo': 'test repo', 'user_id': 1, 'grade': 10}

        # test with no authentication
        response = client.post(
            '/api/activities/', activity_data, format='json')
        self.assertEqual(response.status_code, 401)

        # create user
        client.post('/api/accounts/', self.student1_data, format='json')

        # login
        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create activity
        response = client.post(
            '/api/activities/', activity_data, format='json')
        activity = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            activity, {'repo': 'test repo', 'user_id': 1, 'id': 1, 'grade': None})

    def test_get_activities_student(self):
        client = APIClient()
        client.post('/api/accounts/', self.student1_data, format='json')

        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 1}

        activity = client.post(
            '/api/activities/', activity_data, format='json').json()
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()

        self.assertEqual(
            activity, {'repo': 'test repo', 'user_id': 1, 'id': 2, 'grade': None})

        activity_list = client.get('/api/activities/').json()

        self.assertEqual(activity_list, [{'repo': 'test repo', 'user_id': 1, 'id': 1, 'grade': None}, {
            'repo': 'test repo', 'user_id': 1, 'id': 2, 'grade': None}])

    def test_student_can_only_see_own_activities(self):
        client = APIClient()
        client.post('/api/accounts/', self.student1_data, format='json')

        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 1}

        # create 2 activities for student 1
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()

        client.post('/api/accounts/', self.student2_data, format='json')

        token = client.post(
            '/api/login/', self.student2_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 2}

        # create 2 activities for student 2
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()

        # student 2 only sees his own
        student_2_activities = client.get('/api/activities/').json()

        self.assertEqual(2, len(student_2_activities))

    def test_facilitator_gets_all_activities(self):
        client = APIClient()
        client.post('/api/accounts/', self.student1_data, format='json')

        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 1}

        # create 2 activities for student 1
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()

        client.post('/api/accounts/', self.student2_data, format='json')

        token = client.post(
            '/api/login/', self.student2_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 2}

        # create 2 activities for student 2
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()

        # student 2 only sees his own
        student_2_activities = client.get('/api/activities/').json()

        self.assertEqual(2, len(student_2_activities))

        # create facilitator user
        client.post('/api/accounts/', self.facilitator_data, format='json')

        token = client.post(
            '/api/login/', self.facilitator_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        all_activities = client.get('/api/activities/').json()

        self.assertEqual(4, len(all_activities))

    def test_facilitator_can_filter_activities(self):
        client = APIClient()
        client.post('/api/accounts/', self.student1_data, format='json')

        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 1}

        # create 2 activities for student 1
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()

        client.post('/api/accounts/', self.student2_data, format='json')

        token = client.post(
            '/api/login/', self.student2_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity_data = {'repo': 'test repo', 'user_id': 2}

        # create 2 activities for student 2
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()
        activity = client.post(
            '/api/activities/', activity_data, format='json').json()

        # student 2 only sees his own
        student_2_activities = client.get('/api/activities/').json()

        self.assertEqual(2, len(student_2_activities))

        # create facilitator user
        client.post('/api/accounts/', self.facilitator_data, format='json')

        token = client.post(
            '/api/login/', self.facilitator_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        all_activities = client.get('/api/activities/').json()

        self.assertEqual(4, len(all_activities))

        filtered_activities = client.get('/api/activities/1/').json()
        self.assertEqual(2, len(filtered_activities))

    def test_facilitator_can_grade_activities(self):
        client = APIClient()
        activity_data = {'repo': 'test repo', 'user_id': 1}

        # test with no authentication
        response = client.post(
            '/api/activities/', activity_data, format='json')
        self.assertEqual(response.status_code, 401)

        # create user
        client.post('/api/accounts/', self.student1_data, format='json')

        # login
        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create activity
        response = client.post(
            '/api/activities/', activity_data, format='json')
        activity = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            activity, {'repo': 'test repo', 'user_id': 1, 'id': 1, 'grade': None})

        client.post('/api/accounts/', self.facilitator_data, format='json')

        token = client.post(
            '/api/login/', self.facilitator_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # facilitator updates activity
        response = client.put('/api/activities/', {'repo': 'test repo',
                                                   'user_id': 1, 'id': 1, 'grade': 90}, format='json')

        # switch to student account
        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        activity = client.get('/api/activities/').json()[0]

        self.assertEqual(activity['grade'], 90)


class TestCourseView(TestCase):
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

        self.student2_data = {
            "username": "student2",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False
        }

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

        self.instructor1_data = {
            "username": "instructor",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True
        }

        self.instructor1_login_data = {
            "username": "instructor",
            "password": "1234",
        }

        self.course_data = {
            'name': 'course1'
        }

    def test_instructor_can_create_course(self):
        client = APIClient()

        client.post('/api/accounts/',
                    self.instructor1_data, format='json')

        token = client.post(
            '/api/login/', self.instructor1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        course = client.post(
            '/api/courses/', self.course_data, format='json').json()

        self.assertEqual(course, {'name': 'course1', 'user_set': [], 'id': 1})

    def test_facilitator_or_student_cannot_create_course(self):
        client = APIClient()

        # create student
        client.post('/api/accounts/', self.student1_data, format='json')

        # login
        token = client.post(
            '/api/login/', self.student1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        status_code = client.post(
            '/api/courses/', self.course_data, format='json').status_code
        self.assertEqual(status_code, 403)

        # create student
        client.post('/api/accounts/', self.facilitator_data, format='json')

        # login
        token = client.post(
            '/api/login/', self.facilitator_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        status_code = client.post(
            '/api/courses/', self.course_data, format='json').status_code
        self.assertEqual(status_code, 403)

    def test_anonymous_can_list_courses(self):
        client = APIClient()

        client.post('/api/accounts/',
                    self.instructor1_data, format='json')

        token = client.post(
            '/api/login/', self.instructor1_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        course = client.post(
            '/api/courses/', self.course_data, format='json').json()

        self.assertEqual(course, {'name': 'course1', 'user_set': [], 'id': 1})

        # reset client -> no login
        client = APIClient()

        course_list = client.get('/api/courses/').json()

        self.assertEqual(len(course_list), 1)

    def test_instructor_can_register_students_on_course(self):

        client = APIClient()

        # create student 1
        client.post('/api/accounts/', self.student1_data, format='json')

        # create student 2
        client.post('/api/accounts/', self.student2_data, format='json')

        # create instructor
        client.post('/api/accounts/',
                    self.instructor1_data, format='json')

        token = client.post(
            '/api/login/', self.instructor1_login_data).json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        course = client.post(
            '/api/courses/', self.course_data, format='json').json()

        self.assertEqual(course, {'name': 'course1', 'user_set': [], 'id': 1})

        response = client.put('/api/courses/registrations/',
                              {"course_id": 1, "user_ids": [1, 2]}, format='json').json()

        self.assertEqual(len(response['user_set']), 2)

        response = client.put('/api/courses/registrations/',
                              {"course_id": 1, "user_ids": [1]}, format='json').json()
        self.assertEqual(len(response['user_set']), 1)
        self.assertEqual(response['user_set'][0]['id'], 1)

        response = client.put('/api/courses/registrations/',
                              {"course_id": 1, "user_ids": [2]}, format='json').json()
        self.assertEqual(len(response['user_set']), 1)
        self.assertEqual(response['user_set'][0]['id'], 2)

        response = client.put('/api/courses/registrations/',
                              {"course_id": 1, "user_ids": []}, format='json').json()
        self.assertEqual(len(response['user_set']), 0)
