from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404

from .forms import BudgetForm, ExpenseForm, ProfileForm

from .models import Budget, Profile

def home(request):
    return render(request, 'core/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # or wherever you want to redirect after successful login
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'core/login.html')

def signup_view(request):
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

def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'core/budget_list.html', {'budgets': budgets})

def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'core/budget_form.html', {'form': form})

def budget_detail(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    expenses = budget.expenses.all()
    return render(request, 'core/budget_detail.html', {'budget': budget, 'expenses': expenses})

def expense_create(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.budget = budget
            expense.save()
            return redirect('budget_detail', budget_id=budget.id)
    else:
        form = ExpenseForm()
    return render(request, 'core/expense_form.html', {'form': form, 'budget': budget})

def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_detail', budget_id=budget.id)
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'core/edit_budget.html', {'form': form})

def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'core/confirm_delete.html', {'budget': budget})


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