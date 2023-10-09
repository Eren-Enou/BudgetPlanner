from django import forms
from core.models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'initial_amount', 'amount_spent', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'initial_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_spent': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
