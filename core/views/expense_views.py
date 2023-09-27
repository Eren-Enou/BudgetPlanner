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

