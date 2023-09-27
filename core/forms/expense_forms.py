from django import forms
from django.db import models
from core.models import Expense
from django.db.models.signals import post_save
from django.dispatch import receiver


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date', 'description', 'category', 'is_recurring', 'frequency', 'next_due_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Checkbox for recurring
            'frequency': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for frequency choices
            'next_due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
@receiver(post_save, sender=Expense)
def update_amount_spent(sender, instance, **kwargs):
    total_expenses = instance.budget.expenses.all().aggregate(sum_amount=models.Sum('amount'))['sum_amount'] or 0
    instance.budget.amount_spent = total_expenses
    instance.budget.save()
