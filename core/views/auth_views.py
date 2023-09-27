
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.db import models

from core.forms import ProfileForm
from core.models import Profile, Expense, Budget

def login_view(request):
    # Check if the request method is POST, which indicates a login attempt.
    if request.method == 'POST':
        
        # Retrieve the username and password from the POST data.
        username = request.POST['username']
        password = request.POST['password']
        
        # Try to authenticate the user with the provided credentials.
        user = authenticate(request, username=username, password=password)
        
        # If authentication is successful (i.e., user object is returned), proceed to log the user in.
        if user is not None:
            login(request, user)
            # Redirect to the home page after successful login.
            return redirect('home')
        else:
            # If authentication failed, render the login template again with an error message.
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    else:
        # If the request method is not POST (typically GET), just display the login form.
        return render(request, 'core/login.html')


def signup_view(request):
    # Check if the request method is POST, which indicates a signup attempt.
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if the passwords match
        if password1 == password2:
            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return render(request, 'core/signup.html', {'error': 'Username already exists'})
            if User.objects.filter(email=email).exists():
                return render(request, 'core/signup.html', {'error': 'Email already in use'})
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password1)
            # Log the user in
            login(request, user)
            return redirect('home')  # redirect to home or any other page
        else:
            return render(request, 'core/signup.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'core/signup.html')
    
def logout_view(request):
    logout(request)
    return render(request, 'core/logout.html')

def profile_view(request):
    # Ensure the user is authenticated before accessing the profile
    if not request.user.is_authenticated:
        # Redirect to login page or show an error
        return redirect('login')

    profile = request.user.profile  # Assumes you have a OneToOne relation with User in your Profile model
    return render(request, 'core/profile.html', {'profile': profile})

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Check if form is being submitted
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful update
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }

    return render(request, 'core/edit_profile.html', context)

@login_required
def dashboard_view(request):
    # Fetch all expenses for the currently logged in user
    user_expenses = Expense.objects.filter(user=request.user)
    
    # Calculate the total expenses for the user
    total_expenses = user_expenses.aggregate(models.Sum('amount'))['amount__sum'] or 0

    # Fetch all budgets related to the user
    user_budgets = Budget.objects.filter(user=request.user)

    # Calculate total savings (remaining amounts for all budgets)
    total_savings = sum([budget.initial_amount - (budget.expenses.aggregate(models.Sum('amount'))['amount__sum'] or 0) for budget in user_budgets])
    

    context = {
        'total_expenses': total_expenses,
        'total_savings': total_savings,
        # 'upcoming_bills': upcoming_bills,
        # 'savings_goals': savings_goals,
        # ... add more context data as needed
    }

    return render(request, 'core/dashboard.html', context)
