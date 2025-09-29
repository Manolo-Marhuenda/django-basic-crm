from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import RegistrationForm, LoginForm



class HomeView(TemplateView):
    template_name = 'general/home.html'


class LoginView(FormView):
    template_name = 'general/login.html'
    form_class = LoginForm
    
    def form_valid(self, form):
        usuario = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=usuario, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido de nuevo {user.username}')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Usuario o contraseña incorrectos')
            return super(LoginView, self).form_invalid(form)
        

class RegisterView(CreateView):
    template_name = 'general/register.html'
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente.")
        return super(RegisterView,self).form_valid(form)

    
class LegalView(TemplateView):
    template_name = 'general/legal.html'


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Has cerrado sesión correctamente.')
    return HttpResponseRedirect(reverse_lazy('home'))