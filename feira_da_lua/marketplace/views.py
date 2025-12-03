from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import SearchForm, ProductFilterForm, MarketPlaceFilterForm, MarketPlaceForm, ProductForm
from . import service
from users.models import SearchHistory, Marketer
import base64
from decimal import Decimal, InvalidOperation


def create_fair(request):
    user = request.user_obj
    if not user:
        return redirect('login')

    try:
        marketer = Marketer.objects.get(user=user)
    except Marketer.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = MarketPlaceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            service.CreateMarketPlace(
                name=data['name'],
                marketer=marketer,
                address=data['address'],
                coordinates=data['coordinates']
            )
            return redirect('my_fairs')
    else:
        form = MarketPlaceForm()

    context = {
        'form': form,
    }
    return render(request, 'create_fair.html', context)



def my_fairs(request):
    user = request.user_obj
    if not user:
        return redirect('login')

    try:
        marketer = Marketer.objects.get(user=user)
    except Marketer.DoesNotExist:
        return redirect('home')

    marketplaces = service.GetMarketPlacesByMarketer(marketer)
    
    context = {
        'marketplaces': marketplaces,
    }
    
    return render(request, 'my_fairs.html', context)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def save_search_history(request, query, search_type, results_count):
    if query:
        user = None
        if hasattr(request, 'user_obj') and request.user_obj:
            user = request.user_obj
        
        SearchHistory.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            session_key=request.session.session_key,
            search_query=query,
            search_type=search_type,
            results_count=results_count
        )


def parse_decimal(value):
    if not value:
        return None
    try:
        cleaned = value.replace(',', '.')
        return float(Decimal(cleaned))
    except (InvalidOperation, ValueError):
        return None


def home(request):
    search_form = SearchForm(request.GET or None)
    product_filter_form = ProductFilterForm(request.GET or None)
    marketplace_filter_form = MarketPlaceFilterForm(request.GET or None)
    
    query = request.GET.get('query', '').strip()
    search_type = request.GET.get('search_type', 'feiras')
    
    marketplaces = []
    products = []
    is_searching = bool(query) or any(
        request.GET.get(k) for k in ['min_rating', 'location', 'user_lat', 'min_price', 'max_price']
    )
    
    if search_type == 'feiras' or not search_type:
        marketplaces = service.GetMarketPlacesWithRatings()
        
        if query:
            searched_mps = service.SearchMarketPlaces(query)
            searched_ids = [mp.id for mp in searched_mps]
            marketplaces = [mp for mp in marketplaces if mp['marketplace'].id in searched_ids]
        
        min_rating = request.GET.get('min_rating')
        if min_rating:
            try:
                min_rating_val = float(min_rating)
                marketplaces = [mp for mp in marketplaces if mp['average_rating'] >= min_rating_val]
            except ValueError:
                pass
        
        location = request.GET.get('location', '').strip()
        if location:
            marketplaces = [
                mp for mp in marketplaces 
                if location.lower() in mp['marketplace'].address.lower()
            ]
        
        user_lat = request.GET.get('user_lat')
        user_lon = request.GET.get('user_lon')
        max_distance = request.GET.get('max_distance', '10')
        
        if user_lat and user_lon:
            try:
                lat = float(user_lat)
                lon = float(user_lon)
                dist = float(max_distance) if max_distance else 10
                
                current_ids = {mp['marketplace'].id for mp in marketplaces}
                nearby = service.FilterMarketPlacesByGPS(lat, lon, dist)
                marketplaces = [mp for mp in nearby if mp['marketplace'].id in current_ids]
            except ValueError:
                pass
        
        sort_by = request.GET.get('filter_type')
        if sort_by == 'rating':
            marketplaces = service.SortMarketPlacesByRating(marketplaces)
        
        if query:
            save_search_history(request, query, 'feiras', len(marketplaces))
    
    elif search_type == 'produtos':
        products_list = service.SearchProducts(query) if query else service.GetAllProducts()
        
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        
        min_p = parse_decimal(min_price)
        max_p = parse_decimal(max_price)
        
        if min_p is not None or max_p is not None:
            products_list = service.FilterProductsByPrice(products_list, min_p, max_p)
        
        products_with_photos = []
        for product in products_list:
            photo_base64 = None
            if product.photo:
                try:
                    if isinstance(product.photo, bytes):
                        photo_base64 = base64.b64encode(product.photo).decode('utf-8')
                    elif hasattr(product.photo, 'tobytes'):
                        photo_base64 = base64.b64encode(product.photo.tobytes()).decode('utf-8')
                    elif hasattr(product.photo, 'read'):
                        photo_base64 = base64.b64encode(product.photo.read()).decode('utf-8')
                except Exception:
                    pass
            
            # Buscar marketplace do feirante
            marketplace = None
            if product.marketer:
                marketplace = service.GetMarketPlacesByMarketer(product.marketer)
                marketplace = marketplace[0] if marketplace else None
            
            products_with_photos.append({
                'product': product,
                'photo_base64': photo_base64,
                'marketplace': marketplace
            })
        products = products_with_photos
        
        if query:
            save_search_history(request, query, 'produtos', len(products))
            
    is_marketer = False
    if request.user_obj:
        is_marketer = Marketer.objects.filter(user=request.user_obj).exists()

    context = {
        'search_form': search_form,
        'product_filter_form': product_filter_form,
        'marketplace_filter_form': marketplace_filter_form,
        'marketplaces': marketplaces,
        'products': products,
        'search_type': search_type,
        'query': query,
        'is_searching': is_searching,
        'is_marketer': is_marketer,
    }
    
    return render(request, 'home.html', context)


def marketplace_detail(request, marketplace_id):
    marketplace = service.GetMarketPlaceById(marketplace_id)
    if not marketplace:
        return render(request, '404.html', status=404)
    
    from users.service import GetAvaliationsByMarketplace
    from users.models import Favorite, Avaliation
    
    reviews = GetAvaliationsByMarketplace(marketplace)
    avg_rating = service.GetMarketPlaceAverageRating(marketplace)
    
    products_list = []
    if marketplace.marketer:
        products_list = service.GetProductsByMarketer(marketplace.marketer)
    
    user = request.user_obj
    favorite_ids = set()
    user_already_reviewed = False
    
    if user:
        favorite_ids = set(Favorite.objects.filter(
            user=user
        ).values_list('product_id', flat=True))
        user_already_reviewed = Avaliation.objects.filter(user=user, marketplace=marketplace).exists()
    
    products_with_photos = []
    for product in products_list:
        photo_base64 = None
        if product.photo:
            try:
                if isinstance(product.photo, bytes):
                    photo_base64 = base64.b64encode(product.photo).decode('utf-8')
                elif hasattr(product.photo, 'tobytes'):
                    photo_base64 = base64.b64encode(product.photo.tobytes()).decode('utf-8')
                elif hasattr(product.photo, 'read'):
                    photo_base64 = base64.b64encode(product.photo.read()).decode('utf-8')
            except Exception:
                pass
        products_with_photos.append({
            'product': product,
            'photo_base64': photo_base64,
            'is_favorite': product.id in favorite_ids
        })
    
    review_message = request.GET.get('review_success')
    review_error = request.GET.get('review_error')
    
    context = {
        'marketplace': marketplace,
        'reviews': reviews,
        'average_rating': round(avg_rating, 1) if avg_rating else 0,
        'reviews_count': len(reviews),
        'products': products_with_photos,
        'user_already_reviewed': user_already_reviewed,
        'review_message': review_message,
        'review_error': review_error,
    }
    
    return render(request, 'marketplace_detail.html', context)


def toggle_favorite(request, product_id):
    from users.models import Favorite
    from marketplace.models import Products
    from django.http import JsonResponse
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Metodo nao permitido'}, status=405)
    
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return JsonResponse({'error': 'Produto nao encontrado'}, status=404)
    
    user = request.user_obj
    if not user:
        return JsonResponse({'error': 'Usuario nao autenticado'}, status=401)
    
    existing = Favorite.objects.filter(user=user, product=product).first()
    
    if existing:
        existing.delete()
        is_favorite = False
    else:
        Favorite.objects.create(user=user, product=product)
        is_favorite = True
    
    return JsonResponse({'is_favorite': is_favorite})


def add_review(request, marketplace_id):
    from django.shortcuts import redirect
    from users.service import CreateAvaliation, GetAvaliationsByMarketplace
    from users.models import Avaliation
    
    if request.method != 'POST':
        return redirect('marketplace_detail', marketplace_id=marketplace_id)
    
    marketplace = service.GetMarketPlaceById(marketplace_id)
    if not marketplace:
        return redirect('home')
    
    user = request.user_obj
    if not user:
        return redirect('login')
    
    if Avaliation.objects.filter(user=user, marketplace=marketplace).exists():
        return redirect('marketplace_detail', marketplace_id=marketplace_id)
    
    grade = request.POST.get('grade')
    comment = request.POST.get('comment', '').strip()
    
    if not grade or not comment:
        return redirect(f'/feira/{marketplace_id}/?review_error=Por favor, selecione uma nota e escreva um comentario.')
    
    try:
        grade = int(grade)
        if grade < 1 or grade > 5:
            raise ValueError
    except (ValueError, TypeError):
        return redirect(f'/feira/{marketplace_id}/?review_error=Nota invalida.')
    
    CreateAvaliation(user=user, marketplace=marketplace, grade=grade, comment=comment)
    
    return redirect(f'/feira/{marketplace_id}/?review_success=Sua avaliacao foi enviada com sucesso!')


def update_review(request, review_id):
    from django.shortcuts import redirect
    from users.service import GetAvaliationById, UpdateAvaliation
    
    review = GetAvaliationById(review_id)
    if not review:
        return redirect('home')
    
    user = request.user_obj
    if not user or review.user.id != user.id:
        return redirect('home')
    
    marketplace_id = review.marketplace.id
    
    if request.method != 'POST':
        return redirect('marketplace_detail', marketplace_id=marketplace_id)
    
    grade = request.POST.get('grade')
    comment = request.POST.get('comment', '').strip()
    
    if not grade or not comment:
        return redirect(f'/feira/{marketplace_id}/?review_error=Por favor, selecione uma nota e escreva um comentario.')
    
    try:
        grade = int(grade)
        if grade < 1 or grade > 5:
            raise ValueError
    except (ValueError, TypeError):
        return redirect(f'/feira/{marketplace_id}/?review_error=Nota invalida.')
    
    UpdateAvaliation(review_id, grade=grade, comment=comment)
    
    return redirect(f'/feira/{marketplace_id}/?review_success=Sua avaliacao foi atualizada com sucesso!')


def delete_review(request, review_id):
    from django.shortcuts import redirect
    from users.service import GetAvaliationById, DeleteAvaliation
    
    review = GetAvaliationById(review_id)
    if not review:
        return redirect('home')
    
    user = request.user_obj
    if not user or review.user.id != user.id:
        return redirect('home')
    
    marketplace_id = review.marketplace.id
    
    if request.method != 'POST':
        return redirect('marketplace_detail', marketplace_id=marketplace_id)
    
    DeleteAvaliation(review_id)
    
    return redirect(f'/feira/{marketplace_id}/?review_success=Sua avaliacao foi removida com sucesso!')


def gps_location(request):
    """
    Página placeholder para implementação futura do GPS.
    """
    return render(request, 'gps_location.html')


def edit_fair(request, marketplace_id):
    """
    View para editar uma feira e seus produtos.
    """
    user = request.user_obj
    if not user:
        return redirect('login')

    try:
        marketer = Marketer.objects.get(user=user)
    except Marketer.DoesNotExist:
        return redirect('home')

    marketplace = service.GetMarketPlaceById(marketplace_id)
    if not marketplace:
        return redirect('my_fairs')

    # Verifica se o feirante é dono da feira
    if marketplace.marketer.pk != marketer.pk:
        return redirect('my_fairs')

    # Processar atualização da feira
    if request.method == 'POST' and 'update_marketplace' in request.POST:
        marketplace_form = MarketPlaceForm(request.POST, instance=marketplace)
        if marketplace_form.is_valid():
            marketplace_form.save()
            return redirect('edit_fair', marketplace_id=marketplace_id)
    else:
        marketplace_form = MarketPlaceForm(instance=marketplace)

    # Processar criação de produto
    if request.method == 'POST' and 'create_product' in request.POST:
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.marketer = marketer
            
            # Processar foto se existir
            if 'photo' in request.FILES:
                photo_file = request.FILES['photo']
                product.photo = photo_file.read()
            
            product.save()
            return redirect('edit_fair', marketplace_id=marketplace_id)
    else:
        product_form = ProductForm()

    # Processar atualização de produto
    if request.method == 'POST' and 'update_product' in request.POST:
        product_id = request.POST.get('product_id')
        if product_id:
            product = service.GetProductById(int(product_id))
            if product and product.marketer.pk == marketer.pk:
                name = request.POST.get('name')
                price = request.POST.get('price')
                
                # Atualizar foto se fornecida
                photo = None
                if 'photo' in request.FILES:
                    photo_file = request.FILES['photo']
                    photo = photo_file.read()
                
                service.UpdateProduct(
                    product_id=int(product_id),
                    name=name,
                    price=price,
                    photo=photo
                )
                return redirect('edit_fair', marketplace_id=marketplace_id)

    # Processar exclusão de produto
    if request.method == 'POST' and 'delete_product' in request.POST:
        product_id = request.POST.get('product_id')
        if product_id:
            product = service.GetProductById(int(product_id))
            if product and product.marketer.pk == marketer.pk:
                service.DeleteProduct(int(product_id))
                return redirect('edit_fair', marketplace_id=marketplace_id)

    # Buscar produtos do feirante
    products_list = service.GetProductsByMarketer(marketer)
    
    # Preparar produtos com fotos e formulários
    products_with_data = []
    for product in products_list:
        photo_base64 = None
        if product.photo:
            try:
                if isinstance(product.photo, bytes):
                    photo_base64 = base64.b64encode(product.photo).decode('utf-8')
                elif hasattr(product.photo, 'tobytes'):
                    photo_base64 = base64.b64encode(product.photo.tobytes()).decode('utf-8')
                elif hasattr(product.photo, 'read'):
                    photo_base64 = base64.b64encode(product.photo.read()).decode('utf-8')
            except Exception:
                pass
        
        # Criar formulário pré-preenchido para cada produto
        product_edit_form = ProductForm(instance=product)
        
        products_with_data.append({
            'product': product,
            'photo_base64': photo_base64,
            'form': product_edit_form
        })

    context = {
        'marketplace': marketplace,
        'marketplace_form': marketplace_form,
        'product_form': product_form,
        'products': products_with_data,
    }
    
    return render(request, 'edit_fair.html', context)
