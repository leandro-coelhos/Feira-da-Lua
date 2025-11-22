from django.test import TestCase
from users.models import User, Marketer
from marketplace.service import CreateMarketPlace


class MarketPlaceServiceTest(TestCase):
    def test_create_marketplace(self):
        # Criar user que será dono do marketer
        user = User.objects.create(
            email="teste@example.com",
            username="tester",
            password="123456",
            complete_name="Tester da Silva"
        )

        # Criar marketer
        marketer = Marketer.objects.create(
            user=user,
            cellphone="61999999999"
        )

        # Criar marketplace usando o service
        marketplace = CreateMarketPlace(
            name="Feira da Lua",
            marketer=marketer,
            address="Rua das Estrelas, 123",
            coordinates="0,0"
        )

        # Testes
        self.assertIsNotNone(marketplace)
        self.assertEqual(marketplace.name, "Feira da Lua")
        self.assertEqual(marketplace.address, "Rua das Estrelas, 123")
        self.assertEqual(marketplace.coordinates, "0,0")
        self.assertEqual(marketplace.marketer, marketer)
