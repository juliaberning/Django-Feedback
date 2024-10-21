from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserProfileForm

def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'feedback/home.html', {'username': username})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Account created for {username}!')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 

            return redirect('home')
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
    # Attempt to get the user's profile
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)  # Create a new instance if it doesn't exist

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)  # Bind form with user profile
        if form.is_valid():
            form.save()  # Save the profile data
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=user_profile)  # Pre-fill the form with existing profile data

    return render(request, 'feedback/profile.html', {'form': form})