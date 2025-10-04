from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','username', 'email', 'password']
    
    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')


class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Tu nombre")
    correo = forms.EmailField(label="Tu correo electrónico")
    mensaje = forms.CharField(widget=forms.Textarea, label="Tu mensaje")