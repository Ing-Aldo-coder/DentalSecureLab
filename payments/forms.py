from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = [
            'patient',
            'date',
            'concept',
            'amount',
            'payment_method',
            'notes',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }