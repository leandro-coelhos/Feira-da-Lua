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