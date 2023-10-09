# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.forms import IncomeForm  # Ensure this import is correct
from core.models import Income

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')  # Redirect to an appropriate view after saving the income
    else:
        form = IncomeForm()
    return render(request, 'core/add_income.html', {'form': form})  # Provide the correct template name


@login_required
def view_income(request):
    # Fetch all income for the currently logged in user
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'core/view_income.html', {'incomes': incomes})

@login_required
def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('view_income')  # Redirect to the page where you list all incomes
    else:
        form = IncomeForm(instance=income)
    return render(request, 'core/edit_income.html', {'form': form})

@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    income.delete()
    return redirect('view_income')  # Redirect to the page where you list all incomes