#Import django
from django import forms
from django.db import models
from core.models import Expense, Bill, Income
from django.db.models.signals import post_save
from django.dispatch import receiver
#ExpenseForm, ModelForm with name TextInput, amount NumberInput, date DateInput, description TextArea, category Select, recurring Checkbox, frequency Select,due Date DateInput 
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

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name', 'amount_due', 'due_date', 'is_paid', 'category', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_due': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }        

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
                
@receiver(post_save, sender=Expense)
def update_amount_spent(sender, instance, **kwargs):
    total_expenses = instance.budget.expenses.all().aggregate(sum_amount=models.Sum('amount'))['sum_amount'] or 0
    instance.budget.amount_spent = total_expenses
    instance.budget.save()
