from django.test import SimpleTestCase
from django.urls import reverse,resolve
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from ..models import Movie,Rating

from ..views import list_movie,rate_movie

class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('firstuser', 'test@example.com', 'testpassword')
        self.test_user2= User.objects.create_user('seconduser', 'test2@example.com', 'testpassword2')
        self.create_url = reverse('register')
        self.login_url=reverse('get_token')
        self.list_movies=reverse('list')
        self.rate_movies=reverse('rate')
        self.show_average_rating=reverse('average')
        self.test_movie=Movie.objects.create(movie_name='movie1',movie_about='good',release_date='1212')

        token,created = Token.objects.get_or_create(user=self.test_user2)
        self.test_user2_token=token

        self.httpfactory = APIRequestFactory()

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'hello',
            'email': 'hello@example.com',
            'password': 'somegoodpassword'
        }

        response = self.client.post(self.create_url , data, format='json')

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data, "success")
        self.assertFalse('password' in response.data)

    def test_with_short_password(self):
        data = {
                'username': 'hello',
                'email': 'hello@example.com',
                'password': 'bad'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
    
    def test_registering_with_existing_username(self):
        data = {
                'username': 'firstuser',
                'email': 'user@example.com',
                'password': 'someotherpassword'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)

    def test_registering_with_existing_email(self):
        data = {
                'username': 'someuser',
                'email': 'test@example.com',
                'password': 'someotherpassword'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)

    def test_registering_without_password(self):
        data = {
                'username': 'someuser',
                'email': 'some@example.com',
                'password': ''
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
     
    
    def test_registering_with_invalid_email(self):
        data={
            "email":"absd",
            "username":"absd",
            "password":"123445798"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)

    def test_login_with_non_existing_username(self):
        data={
        "username":"Ajay",
        "password":"ajay123456"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Invalid Credentials")

    def test_login_with_wrong_password(self):
        data={
             "username":"firstuser",
             "password":"wrongpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'],"Invalid Credentials" )

    def test_login_with_valid_credentials(self):
        data={
            "username":"firstuser",
            "password":"testpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['token']),40 )

    def test_listing_movies_with_correct_token(self):
        request = self.httpfactory.get(self.list_movies , format='json')
        force_authenticate(request, user=self.test_user2)
        view = list_movie
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        
    def test_listing_movies_without_token(self):
        request = self.httpfactory.get(self.list_movies , format='json')
        view = list_movie
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

    def test_rating_movies_with_correct_token(self):
        data={
        "movie":"movie1",
        "rating":"8"
        }
        request = self.httpfactory.post(self.rate_movies, data, format='json')
        force_authenticate(request, user=self.test_user2)
        view = rate_movie
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_rating_movies_without_token(self):
        data={
        "movie":"movie1",
        "rating":"8"
        }
        request = self.httpfactory.post(self.rate_movies, data, format='json')
        view = rate_movie
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rating_movies_with_wrong_movie_name(self):
        data={
            "movie":"unknown",
            "rating":"2"
        }
        request = self.httpfactory.post(self.rate_movies, data, format='json')
        force_authenticate(request, user=self.test_user2)
        view = rate_movie
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)






    

    

        

    

    




