# Django Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models

# Plotly Imports (for your budget_detail view's chart)
import plotly.offline as opy
import plotly.graph_objs as go

# Your App Imports
from core.forms import BudgetForm, ExpenseForm
from core.models import Budget


def home(request):
    # Ensure the user is logged in before accessing the view.
    if request.user.is_authenticated:

        # Fetch the latest budget associated with the current user based on its creation date.
        latest_budget = Budget.objects.filter(user=request.user).order_by('creation_date').first()

        # If there's a latest budget, fetch the associated expenses; otherwise, set expenses to an empty list.
        if latest_budget:
            expenses_for_latest_budget = latest_budget.expenses.all()
        else:
            expenses_for_latest_budget = []

        # ... your other view logic ...

        # Prepare the context dictionary with budget and associated expenses (and other data if present) to render the template.
        context = {
            'latest_budget': latest_budget,
            'expenses': expenses_for_latest_budget,
            # ... your other context variables ...
        }

        # Render the 'core/home.html' template using the prepared context.
        return render(request, 'core/home.html', context)



def budget_list(request):
    # Fetch budgets related to the current user.
    budgets = Budget.objects.filter(user=request.user)
    
    # List to store budgets along with their remaining amounts.
    budgets_with_remaining = []
    
    for budget in budgets:
        # Get the sum of all expenses related to this budget.
        total_expenses = budget.expenses.all().aggregate(sum_amount=models.Sum('amount'))['sum_amount'] or 0
        
        # Compute the remaining amount.
        remaining = budget.initial_amount - total_expenses
        
        # Append the budget and its remaining amount to our list.
        budgets_with_remaining.append({
            'budget': budget,
            'remaining': remaining
        })

    return render(request, 'core/budget_list.html', {'budgets_with_remaining': budgets_with_remaining})


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
    # Fetch the Budget object with the given budget_id or return a 404 error if not found.
    budget = get_object_or_404(Budget, id=budget_id)

    # Get all the expenses associated with the fetched budget.
    expenses = budget.expenses.all()
    amount_remaining = budget.initial_amount - budget.amount_spent

    # Create a bar chart using Plotly with two bars: one for total expenses and another for the initial budget amount.
    # The bars are colored red for expenses and green for the initial budget for visual differentiation.
    trace1 = go.Bar(x=['Expenses', 'Initial Budget'], 
                    y=[sum([expense.amount for expense in expenses]), budget.initial_amount],
                    marker=dict(color=['red', 'green']))

    # Define the layout for the chart with a title.
    layout = go.Layout(title='Budget vs Expenses')

    # Combine the trace and layout to create a figure.
    figure = go.Figure(data=[trace1], layout=layout)

    # Convert the figure to a div element so it can be embedded in the Django template. 
    # This will not automatically open a new tab/window for the plot.
    div = opy.plot(figure, auto_open=False, output_type='div')

    # Render the 'core/budget_detail.html' template with the budget, associated expenses, and the embedded plot.
    return render(request, 'core/budget_detail.html', {'budget': budget, 'expenses': expenses, 'plot_div': div, 'amount_remaining':amount_remaining})

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


