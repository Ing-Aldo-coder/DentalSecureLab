from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'phone',
            'email',
            'address',
        ]

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }