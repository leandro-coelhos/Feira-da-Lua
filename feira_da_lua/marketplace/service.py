from .models import MarketPlace, Products
from users.models import Marketer, Avaliation
from django.db.models import Avg, Q
import math

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

def GetMarketPlaceById(marketplace_id: int) -> MarketPlace | None:
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
    try:
        marketplace = MarketPlace.objects.get(id=marketplace_id)
    except MarketPlace.DoesNotExist:
        return None

    if name is not None:
        marketplace.name = name

    if address is not None:
        marketplace.address = address

    if coordinates is not None:
        marketplace.coordinates = coordinates

    marketplace.save()
    return marketplace

def DeleteMarketPlace(marketplace_id: int) -> bool:
    """
    Deleta um marketplace pelo ID.

    @param marketplace_id: ID do marketplace a ser deletado.
    @return True se deletou com sucesso, False se não existir.
    """
    marketplace = GetMarketPlaceById(marketplace_id)

    if marketplace is None:
        return False

    marketplace.delete()
    return True


# Funcoes de Busca e Filtro

def SearchMarketPlaces(query: str = None) -> list:
    """
    Busca marketplaces por nome ou endereco.
    """
    if not query:
        return list(MarketPlace.objects.all())
    
    return list(MarketPlace.objects.filter(
        Q(name__icontains=query) | Q(address__icontains=query)
    ))


def SearchProducts(query: str = None) -> list:
    """
    Busca produtos por nome.
    """
    if not query:
        return list(Products.objects.all())
    
    return list(Products.objects.filter(name__icontains=query))


def FilterProductsByPrice(products: list = None, min_price: float = None, max_price: float = None) -> list:
    """
    Filtra produtos por faixa de preco.
    """
    if products is None:
        queryset = Products.objects.all()
    else:
        product_ids = [p.id for p in products]
        queryset = Products.objects.filter(id__in=product_ids)
    
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)
    
    return list(queryset)


def GetMarketPlaceAverageRating(marketplace: MarketPlace) -> float:
    """
    Calcula a nota media de um marketplace.
    """
    avg = Avaliation.objects.filter(marketplace=marketplace).aggregate(Avg('grade'))
    return avg['grade__avg'] or 0


def GetMarketPlacesWithRatings() -> list:
    """
    Retorna todos os marketplaces com suas notas medias.
    """
    marketplaces = MarketPlace.objects.all()
    result = []
    for mp in marketplaces:
        avg_rating = GetMarketPlaceAverageRating(mp)
        result.append({
            'marketplace': mp,
            'average_rating': round(avg_rating, 1) if avg_rating else 0,
            'reviews_count': Avaliation.objects.filter(marketplace=mp).count()
        })
    return result


def FilterMarketPlacesByRating(min_rating: float = None) -> list:
    """
    Filtra marketplaces por nota media minima.
    """
    all_with_ratings = GetMarketPlacesWithRatings()
    if min_rating is None:
        return all_with_ratings
    
    return [mp for mp in all_with_ratings if mp['average_rating'] >= min_rating]


def FilterMarketPlacesByAddress(address_query: str) -> list:
    """
    Filtra marketplaces por endereco.
    """
    marketplaces = MarketPlace.objects.filter(address__icontains=address_query)
    result = []
    for mp in marketplaces:
        avg_rating = GetMarketPlaceAverageRating(mp)
        result.append({
            'marketplace': mp,
            'average_rating': round(avg_rating, 1) if avg_rating else 0,
            'reviews_count': Avaliation.objects.filter(marketplace=mp).count()
        })
    return result


def CalculateDistance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distancia entre dois pontos usando a formula de Haversine.
    Retorna a distancia em km.
    """
    R = 6371  # Raio da Terra em km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def FilterMarketPlacesByGPS(user_lat: float, user_lon: float, max_distance_km: float = 10) -> list:
    """
    Filtra marketplaces por proximidade GPS.
    """
    all_marketplaces = MarketPlace.objects.all()
    result = []
    
    for mp in all_marketplaces:
        try:
            coords = mp.coordinates.split(',')
            mp_lat = float(coords[0].strip())
            mp_lon = float(coords[1].strip())
            distance = CalculateDistance(user_lat, user_lon, mp_lat, mp_lon)
            
            if distance <= max_distance_km:
                avg_rating = GetMarketPlaceAverageRating(mp)
                result.append({
                    'marketplace': mp,
                    'average_rating': round(avg_rating, 1) if avg_rating else 0,
                    'reviews_count': Avaliation.objects.filter(marketplace=mp).count(),
                    'distance': round(distance, 1)
                })
        except (ValueError, IndexError):
            continue
    
    result.sort(key=lambda x: x['distance'])
    return result


def SortMarketPlacesByRating(marketplaces_data: list, descending: bool = True) -> list:
    """
    Ordena lista de marketplaces por nota media.
    """
    return sorted(marketplaces_data, key=lambda x: x['average_rating'], reverse=descending)


# Funcoes de Produtos

def GetAllProducts() -> list:
    """
    Retorna todos os produtos.
    """
    return list(Products.objects.all())


def GetProductsByMarketer(marketer: Marketer) -> list:
    """
    Retorna produtos de um feirante especifico.
    """
    return list(Products.objects.filter(marketer=marketer))


def GetMarketPlacesByMarketer(marketer: Marketer) -> list:
    """
    Retorna as feiras de um feirante especifico.
    """
    return list(MarketPlace.objects.filter(marketer=marketer))


def GetProductById(product_id: int) -> Products | None:
    """
    Obtém um produto pelo seu ID.
    """
    try:
        return Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return None

def DeleteProduct(product_id: int) -> bool:
    """
    Deleta um produto pelo ID.
    """
    product = GetProductById(product_id)
    if product is None:
        return False
    product.delete()
    return True

def CreateProduct(marketer: Marketer, name: str, price: float, photo: any) -> Products:
    """
    Cria um novo produto.
    """
    product = Products(
        marketer=marketer,
        name=name,
        price=price,
        photo=photo
    )
    product.save()
    return product

def UpdateProduct(product_id: int, name=None, price=None, photo=None) -> Products | None:
    """
    Atualiza um produto existente.
    """
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return None

    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if photo is not None:
        product.photo = photo

    product.save()
    return product


