from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm, MarketerRegistrationForm
from .service import GetUserByEmail, CreateUser, CreateMarketer
from .models import User
from feira_da_lua.marketplace.models import MarketPlace
from .service import CreateAvaliation, DeleteAvaliation, UpdateAvaliation, GetAvaliationsByMarketplace, GetAvaliationById
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def IndexPage(request):
    return redirect('home')

def RegistroPage(request):
    return render(request, 'registro.html')

def LoginUser(request):
    if request.session.get('user_id'):
        return redirect('home')
    
    if request.method == 'POST':
        formulario = UserLoginForm(request.POST)
        if formulario.is_valid():
            email = formulario.cleaned_data['email']
            password = formulario.cleaned_data['password']

            user = GetUserByEmail(email)
            if user and user.password == password:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                print('Login falhou: usuario nao encontrado ou senha incorreta')
                messages.error(request, 'Email ou senha incorretos.')
    return render(request, 'login.html', {'form': UserLoginForm()})

def RegisterUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            complete_name = form.cleaned_data['complete_name']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este email ja esta em uso.')
                return render(request, 'cadastro_cliente.html', {'form': form})

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Este nome de usuario ja esta em uso.')
                return render(request, 'cadastro_cliente.html', {'form': form})

            user = CreateUser(email=email, username=username, password=password, complete_name=complete_name)
            messages.success(request, 'Conta criada com sucesso! Faca login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserRegistrationForm()

    return render(request, 'cadastro_cliente.html', {'form': form})

def RegisterMarketer(request):
    if request.method == 'POST':
        form = MarketerRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            complete_name = form.cleaned_data['complete_name']
            password = form.cleaned_data['password']
            cellphone = form.cleaned_data['cellphone']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este email ja esta em uso.')
                return render(request, 'cadastro_feirante.html', {'form': form})

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Este nome de usuario ja esta em uso.')
                return render(request, 'cadastro_feirante.html', {'form': form})

            marketer = CreateMarketer(email=email, username=username, password=password, complete_name=complete_name, cellphone=cellphone)
            messages.success(request, 'Conta de feirante criada com sucesso! Faca login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = MarketerRegistrationForm()

    return render(request, 'cadastro_feirante.html', {'form': form})

def LogoutUser(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')


def FavoritesPage(request):
    from users.models import Favorite
    import base64
    
    user = request.user_obj
    favorites = Favorite.objects.filter(user=user).select_related('product', 'product__marketer', 'product__marketer__user')
    
    favorites_with_photos = []
    for fav in favorites:
        photo_base64 = None
        if fav.product.photo:
            try:
                if isinstance(fav.product.photo, bytes):
                    photo_base64 = base64.b64encode(fav.product.photo).decode('utf-8')
                elif hasattr(fav.product.photo, 'tobytes'):
                    photo_base64 = base64.b64encode(fav.product.photo.tobytes()).decode('utf-8')
            except Exception:
                pass
        favorites_with_photos.append({
            'favorite': fav,
            'product': fav.product,
            'photo_base64': photo_base64
        })
    
    return render(request, 'favoritos.html', {'favorites': favorites_with_photos, 'user': user})

def ProfileUser(View):
    pass

def DeleteUser(View):
    pass

def UpdateUser(View):
    pass

def ListUsers(View):
    pass

@login_required
def CreateComment(request):
    if request.method == 'POST':
        marketplace_id = request.POST.get('marketplace_id')
        grade = request.POST.get('grade')
        comment = request.POST.get('comment')
        
        marketplace = get_object_or_404(MarketPlace, id=marketplace_id)
        
        CreateAvaliation(
            user=request.user, 
            marketplace=marketplace, 
            grade=int(grade), 
            comment=comment
        )
        
        return redirect(f'/comment/list/?marketplace_id={marketplace_id}')

    marketplace_id = request.GET.get('marketplace_id')
    return render(request, 'avaliation_form.html', {'marketplace_id': marketplace_id})


@login_required
def DeleteComment(request):
    if request.method == 'POST':
        avaliation_id = request.POST.get('avaliation_id')
        
        avaliation = GetAvaliationById(avaliation_id)
        if avaliation and avaliation.user == request.user:
            marketplace_id = avaliation.marketplace.id
            DeleteAvaliation(avaliation_id)
            return redirect(f'/comment/list/?marketplace_id={marketplace_id}')
    
    avaliation_id = request.GET.get('avaliation_id')
    avaliation = GetAvaliationById(avaliation_id)
    return render(request, 'avaliation_confirm_delete.html', {'avaliation': avaliation})


@login_required
def UpdateComment(request):
    if request.method == 'POST':
        avaliation_id = request.POST.get('avaliation_id')
        grade = request.POST.get('grade')
        comment = request.POST.get('comment')
        
        avaliation = GetAvaliationById(avaliation_id)
        
        if avaliation and avaliation.user == request.user:
            UpdateAvaliation(avaliation_id, grade=int(grade), comment=comment)
            return redirect(f'/comment/list/?marketplace_id={avaliation.marketplace.id}')

    avaliation_id = request.GET.get('avaliation_id')
    avaliation = GetAvaliationById(avaliation_id)
    return render(request, 'avaliation_update.html', {'avaliation': avaliation})


def ListComments(request):
    marketplace_id = request.GET.get('marketplace_id')
    
    if marketplace_id:
        marketplace = get_object_or_404(MarketPlace, id=marketplace_id)
        avaliations = GetAvaliationsByMarketplace(marketplace)
        context = {
            'avaliations': avaliations,
            'marketplace': marketplace
        }
        return render(request, 'avaliation_list.html', context)
    
    return redirect('list_users')