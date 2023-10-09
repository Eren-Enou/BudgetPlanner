# Django Imports

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models

# Plotly Imports (for your budget_detail view's chart)
import plotly.offline as opy
import plotly.graph_objs as go

# Your App Imports
from core.forms import BudgetForm, ExpenseForm
from core.models import Budget


@login_required
def home(request):
    # Fetch all budgets for the currently logged in user
    user_budgets = Budget.objects.filter(user=request.user).order_by('-id')

    # Get the selected budget id from the query parameters, if present
    selected_budget_id = request.GET.get('budget_id')

    # Fetch the selected budget if an id is provided, otherwise get the latest budget
    if selected_budget_id:
        selected_budget = get_object_or_404(Budget, id=selected_budget_id, user=request.user)
    else:
        selected_budget = user_budgets.first()

        
    # If there's a selected budget, fetch the associated expenses; otherwise, set expenses to an empty list
    if selected_budget:
        expenses_for_selected_budget = selected_budget.expenses.all()
        total_amount = selected_budget.initial_amount - selected_budget.amount_spent  # Calculating the remaining amount
    else:
        expenses_for_selected_budget = []
        total_amount = 0  # or you can set it to None or any default value

# Prepare the context dictionary with selected budget, associated expenses, total remaining amount, and all budgets to render the template
    context = {
        'selected_budget': selected_budget,
        'expenses': expenses_for_selected_budget,
        'all_budgets': user_budgets,
        'total_amount': total_amount,  # Including the total_amount in the context
        'latest_budget': user_budgets.first(),  # This line is added
    }

    # Render the 'core/home.html' template using the prepared context
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

    request.session['last_accessed_budget'] = budget_id

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



def get_total_amount(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    total_amount = budget.initial_amount - budget.amount_spent
    return JsonResponse({'total_amount': total_amount})

def get_budget_data(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    expenses = budget.expenses.all().values('name', 'amount')  # Adjust field names as needed
    total_amount = budget.initial_amount - budget.amount_spent
    data = {
        'total_amount': str(total_amount),  # Convert Decimal to string to make it serializable
        'budget_name': budget.name,
        'expenses': list(expenses),
    }
    return JsonResponse(data)