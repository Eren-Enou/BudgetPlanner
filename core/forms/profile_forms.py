from django import forms
from core.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'phone_number', 'date_of_birth', 'bio', 'location', 'website']