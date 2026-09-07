from django import forms
from .models import Client, Interaction

class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name','last_name', 'email', 'phone', 'company']


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'company', 'assigned_commercials']
        widgets = {
            'assigned_commercials': forms.CheckboxSelectMultiple(),
        }


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['type', 'interaction_date', 'notes']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'interaction_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe los detalles de la interacción...'}),
        }