from django.test import TestCase
from users.models import User, Marketer
from marketplace.service import (
    CreateMarketPlace,
    GetMarketplaceById,
    GetAllMarketPlaces
)


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


class MarketPlaceServiceReadTest(TestCase):

    def setUp(self):
        # Criar user
        self.user = User.objects.create(
            email="teste@example.com",
            username="tester",
            password="123456",
            complete_name="Tester da Silva"
        )

        # Criar marketer
        self.marketer = Marketer.objects.create(
            user=self.user,
            cellphone="61999999999"
        )

        # Criar marketplaces
        self.market1 = CreateMarketPlace(
            name="Feira da Lua",
            marketer=self.marketer,
            address="Rua A",
            coordinates="1,1"
        )

        self.market2 = CreateMarketPlace(
            name="Feira do Sol",
            marketer=self.marketer,
            address="Rua B",
            coordinates="2,2"
        )

    def test_get_marketplace_by_id(self):
        marketplace = GetMarketplaceById(self.market1.id)

        self.assertIsNotNone(marketplace)
        self.assertEqual(marketplace.id, self.market1.id)
        self.assertEqual(marketplace.name, "Feira da Lua")

    def test_get_marketplace_by_id_not_found(self):
        marketplace = GetMarketplaceById(999)  # inexistente
        self.assertIsNone(marketplace)

    def test_get_all_marketplaces(self):
        marketplaces = GetAllMarketPlaces()

        self.assertEqual(len(marketplaces), 2)
        self.assertIn(self.market1, marketplaces)
        self.assertIn(self.market2, marketplaces)
