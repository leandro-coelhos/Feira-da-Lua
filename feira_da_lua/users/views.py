from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm
from .service import GetUserByEmail
from marketplace.models import MarketPlace
from .service import CreateAvaliation, DeleteAvaliation, UpdateAvaliation, GetAvaliationsByMarketplace, GetAvaliationById
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def LoginUser(request):
    if request.method == 'POST':
        formulario = UserLoginForm(request.POST)
        if formulario.is_valid():
            email = formulario.cleaned_data['email']
            password = formulario.cleaned_data['senha']

            user = GetUserByEmail(email)
            if user and user.password == password:
                return redirect('profile', user_id=user.id)
    return render(request, 'users/login.html', {'form': UserLoginForm()})

def RegisterUser(View):
    pass

def LogoutUser(View):
    pass

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