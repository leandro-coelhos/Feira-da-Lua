from .models import MarketPlace
from users.models import Marketer

def CreateMarketPlace(name: str, marketer: Marketer, address: str, coordinates: str) -> MarketPlace:
    """
    Cria um novo marketplace.

    @param name: Nome do marketplace.
    @param marketer: Objeto Marketer associado ao marketplace.
    @param address: Endereço do marketplace.
    @param coordinates: Coordenadas do marketplace.

    @return O objeto MarketPlace criado.
    """
    marketplace = MarketPlace(
        name=name,
        marketer=marketer,
        address=address,
        coordinates=coordinates
    )
    marketplace.save()
    return marketplace

def GetMarketplaceById(marketplace_id: int) -> MarketPlace | None:
    """
    Obtém um marketplace pelo seu ID.

    @param marketplace_id: ID do marketplace a ser buscado.
    @return O objeto MarketPlace correspondente ao ID informado, 
            ou None caso não exista.
    """
    try:
        return MarketPlace.objects.get(id=marketplace_id)
    except MarketPlace.DoesNotExist:
        return None


def GetAllMarketPlaces() -> list[MarketPlace]:
    """
    Retorna todos os marketplaces cadastrados.

    @return Uma lista contendo todos os objetos MarketPlace existentes.
    """
    return list(MarketPlace.objects.all())

def UpdateMarketPlace(marketplace_id: int, name=None, address=None, coordinates=None):
    """
    Atualiza um marketplace existente.

    @param marketplace_id: ID do marketplace a ser atualizado.
    @param name: Novo nome (opcional).
    @param address: Novo endereço (opcional).
    @param coordinates: Novas coordenadas (opcional).

    @return O objeto atualizado, ou None caso não exista.
    """
    pass
