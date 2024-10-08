from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'feedback/home.html', {'username': username})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'feedback/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'feedback/login.html')

def logout_view(request):
    logout(request)
    return redirect('login') 


@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    return render(request, 'feedback/profile.html', {'user_profile': user_profile})