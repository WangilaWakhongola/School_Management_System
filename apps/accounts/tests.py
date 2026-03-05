from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email='admin@test.com',
            password='Admin@123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        self.teacher = User.objects.create_user(
            email='teacher@test.com',
            password='Teacher@123',
            first_name='Jane',
            last_name='Doe',
            role='teacher'
        )

    def get_token(self, email, password):
        res = self.client.post('/api/auth/login/', {'email': email, 'password': password})
        return res.data.get('access')

    def test_login_success(self):
        res = self.client.post('/api/auth/login/', {
            'email': 'admin@test.com',
            'password': 'Admin@123'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_login_invalid_credentials(self):
        res = self.client.post('/api/auth/login/', {
            'email': 'admin@test.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authenticated(self):
        token = self.get_token('admin@test.com', 'Admin@123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.get('/api/auth/profile/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], 'admin@test.com')

    def test_profile_unauthenticated(self):
        res = self.client.get('/api/auth/profile/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_as_admin(self):
        token = self.get_token('admin@test.com', 'Admin@123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.post('/api/auth/register/', {
            'email': 'newstudent@test.com',
            'first_name': 'New',
            'last_name': 'Student',
            'password': 'Student@123',
            'confirm_password': 'Student@123',
            'role': 'student'
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_register_as_teacher_forbidden(self):
        token = self.get_token('teacher@test.com', 'Teacher@123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.post('/api/auth/register/', {
            'email': 'another@test.com',
            'first_name': 'Another',
            'last_name': 'User',
            'password': 'Test@123',
            'confirm_password': 'Test@123',
            'role': 'student'
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
