from django.test import TestCase
from .service import CreateUser, GetUserById, GetUserByEmail, UpdateUser, DeleteUser
from .service import CreateMarketer, GetMarketerById, GetMarketerByEmail, UpdateMarketer, DeleteMarketer
from .service import CreateAvaliation, GetAvaliationById, GetAvaliationsByUser, GetAvaliationsByMarketplace
from .service import UpdateAvaliation, DeleteAvaliation
from feira_da_lua.marketplace.models import MarketPlace

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
          UpdateUser(user.id, username="newusername", complete_name="New Name", password="newpassword")
          user = GetUserById(user.id)
          self.assertEqual(user.username, "newusername")
          self.assertEqual(user.complete_name, "New Name")
          self.assertEqual(user.password, "newpassword")
     def test_delete_user(self):
          user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
          user_id = user.id
          DeleteUser(user_id)
          self.assertIsNone(GetUserById(user_id))

class MarketerServiceTest(TestCase):
     def test_create_marketer(self):
          marketer = CreateMarketer(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva", cellphone="123456789")
          self.assertIsNotNone(marketer)
     def test_get_marketer(self):
          marketer = CreateMarketer(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva", cellphone="123456789")
          self.assertEqual(marketer, GetMarketerById(marketer.user.id))
          self.assertEqual(marketer, GetMarketerByEmail(marketer.user.email))
     def test_update_marketer(self):
          marketer = CreateMarketer(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva", cellphone="123456789")
          UpdateMarketer(marketer.user.id, username="newusername", complete_name="New Name", password="newpassword", cellphone="987654321")
          marketer = GetMarketerById(marketer.user.id)
          self.assertEqual(marketer.user.username, "newusername")
          self.assertEqual(marketer.user.complete_name, "New Name")
          self.assertEqual(marketer.user.password, "newpassword")
          self.assertEqual(marketer.cellphone, "987654321")
     def test_delete_marketer(self):
          marketer = CreateMarketer(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva", cellphone="123456789")
          marketer_id = marketer.user.id
          DeleteMarketer(marketer_id)
          self.assertIsNone(GetMarketerById(marketer_id))

class AvaliationServiceTest(TestCase):
     def test_create_avaliation(self):
          user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
          marketePlace = MarketPlace(name="Feira da Lua", marketer=None, address="Some Address", coordinates="0,0")
          MarketPlace.save(marketePlace)
          avaliation = CreateAvaliation(user=user, marketplace=marketePlace, grade=5, comment="Great marketplace!")
          self.assertIsNotNone(avaliation)

     def test_get_avaliation(self):
          user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
          marketePlace = MarketPlace(name="Feira da Lua", marketer=None, address="Some Address", coordinates="0,0")
          MarketPlace.save(marketePlace)
          avaliation = CreateAvaliation(user=user, marketplace=marketePlace, grade=5, comment="Great marketplace!")
          self.assertEqual(avaliation, GetAvaliationById(avaliation.id))
          self.assertEqual(avaliation, GetAvaliationsByUser(user)[0])
          self.assertEqual(avaliation, GetAvaliationsByMarketplace(marketePlace)[0])
     
     def test_update_avaliation(self):
          user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
          marketePlace = MarketPlace(name="Feira da Lua", marketer=None, address="Some Address", coordinates="0,0")
          MarketPlace.save(marketePlace)
          avaliation = CreateAvaliation(user=user, marketplace=marketePlace, grade=5, comment="Great marketplace!")
          UpdateAvaliation(avaliation.id, grade=4, comment="Good marketplace.")
          avaliation = GetAvaliationById(avaliation.id)
          self.assertEqual(avaliation.grade, 4)
          self.assertEqual(avaliation.comment, "Good marketplace.")

     def test_delete_avaliation(self):
          user = CreateUser(email="leandrocs1500@gmail.com", username="leandrocs1500", password="securepassword", complete_name="Leandro Coelho Silva")
          marketePlace = MarketPlace(name="Feira da Lua", marketer=None, address="Some Address", coordinates="0,0")
          MarketPlace.save(marketePlace)
          avaliation = CreateAvaliation(user=user, marketplace=marketePlace, grade=5, comment="Great marketplace!")
          avaliation_id = avaliation.id
          DeleteAvaliation(avaliation_id)
          self.assertIsNone(GetAvaliationById(avaliation_id))

# Create your tests here.
