from django.test import TestCase
from feira_da_lua.users.models import User, Marketer
from feira_da_lua.marketplace.service import (
    CreateMarketPlace,
    GetMarketplaceById,
    GetAllMarketPlaces,
    UpdateMarketPlace,
    DeleteMarketPlace
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

class MarketPlaceServiceUpdateTest(TestCase):

    def setUp(self):
        # Criar user
        self.user = User.objects.create(
            email="update@example.com",
            username="update_user",
            password="123456",
            complete_name="User Update"
        )

        # Criar marketer
        self.marketer = Marketer.objects.create(
            user=self.user,
            cellphone="61988888888"
        )

        # Criar marketplace inicial
        self.marketplace = CreateMarketPlace(
            name="Feira Antiga",
            marketer=self.marketer,
            address="Rua Velha",
            coordinates="1,1"
        )

    def test_update_marketplace(self):
        updated = UpdateMarketPlace(
            marketplace_id=self.marketplace.id,
            name="Feira Nova",
            address="Rua Nova",
            coordinates="2,2"
        )

        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "Feira Nova")
        self.assertEqual(updated.address, "Rua Nova")
        self.assertEqual(updated.coordinates, "2,2")

    def test_partial_update_marketplace(self):
        updated = UpdateMarketPlace(
            marketplace_id=self.marketplace.id,
            address="Rua Atualizada"
        )

        self.assertIsNotNone(updated)
        self.assertEqual(updated.address, "Rua Atualizada")
        # Campos não passados devem permanecer iguais
        self.assertEqual(updated.name, "Feira Antiga")

    def test_update_marketplace_not_found(self):
        updated = UpdateMarketPlace(
            marketplace_id=999,
            name="Inexistente"
        )

        self.assertIsNone(updated)

class MarketPlaceServiceDeleteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="del@example.com",
            username="del_user",
            password="123456",
            complete_name="User Delete"
        )

        self.marketer = Marketer.objects.create(
            user=self.user,
            cellphone="61977777777"
        )

        self.marketplace = CreateMarketPlace(
            name="Feira Delete",
            marketer=self.marketer,
            address="Rua X",
            coordinates="10,10"
        )

    def test_delete_marketplace(self):
        deleted = DeleteMarketPlace(self.marketplace.id)

        self.assertTrue(deleted)
        self.assertIsNone(GetMarketplaceById(self.marketplace.id))

    def test_delete_marketplace_not_found(self):
        deleted = DeleteMarketPlace(999)

        self.assertFalse(deleted)
