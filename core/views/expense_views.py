# Django Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Your App Imports
from core.forms import ExpenseForm
from core.models import Expense, Budget


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