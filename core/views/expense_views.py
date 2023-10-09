# Django Imports

from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Your App Imports
from core.forms import ExpenseForm, BillForm, IncomeForm
from core.models import Expense, Budget, Income

@login_required
def expense_create(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    
    # Check if the budget belongs to the user
    if budget.user != request.user:
        return HttpResponseForbidden("You don't have permission to access this resource.")

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.budget = budget
            expense.user = request.user
            expense.save()
            return redirect('budget_detail', budget_id=budget.id)
    else:
        form = ExpenseForm()

    return render(request, 'core/expense_form.html', {'form': form, 'budget': budget})

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('budget_detail', budget_id=expense.budget.id)
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'core/edit_expense.html', {'form': form})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('budget_detail', budget_id=expense.budget.id)
    return render(request, 'core/confirm_delete_expense.html', {'expense': expense})


def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, 'Bill added successfully')  # success message
            return redirect('dashboard')  # redirect to the dashboard or another appropriate page after saving the bill
        else:
            print(form.errors)  # Print errors to console for debugging
            messages.error(request, 'Error adding bill')  # error message
    else:
        form = BillForm()

    return render(request, 'core/create_bill.html', {'form': form})

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})