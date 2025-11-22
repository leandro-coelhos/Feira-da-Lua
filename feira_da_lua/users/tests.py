from django.test import TestCase
from .service import CreateUser, GetUserById, GetUserByEmail
# Service tests

class UserServiceTest(TestCase):
     def test_create_user(self):
          user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
          self.assertIsNotNone(user)
     def test_get(self):
          user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
          self.assertEqual(user, GetUserById(user.id))
          self.assertEqual(user, GetUserByEmail(user.email))
     def test_update_user(self):
          user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
          UpdateUser(user.id, usarnme="newusername", complete_name="New Name")
          self.assertEqual(user.username, "newusername")
          self.assertEqual(user.complete_name, "New Name")
                
# Create your tests here.
