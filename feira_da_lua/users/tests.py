from django.test import TestCase
from .service import CreateUser
# Service tests

class UserServiceTest(TestCase):
     def test_create_user(self):
         user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
         self.assertIsNotNone(user)
     
     
      
# Create your tests here.
