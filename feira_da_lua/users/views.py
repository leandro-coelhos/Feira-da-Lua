from django.shortcuts import render, redirect
from django.views import View
from .forms import UserLoginForm
from .service import GetUserByEmail

def LoginUser(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

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

def CreateComment(View):
    pass

def DeleteComment(View):
    pass

def UpdateComment(View):
    pass

def ListComments(View):
     pass

# Create your views here.
