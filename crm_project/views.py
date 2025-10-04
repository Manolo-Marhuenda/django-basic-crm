from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import RegistrationForm, LoginForm, ContactoForm
from management.models import Company
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render



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
            return HttpResponseRedirect(reverse_lazy('dashboard'))
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


def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Aquí va la lógica para procesar el formulario
             # Obtener los datos del formulario
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']

            # Construir el asunto y el cuerpo del correo
            asunto = f'Mensaje de contacto de {nombre}'
            cuerpo = f'De: {nombre} <{correo}>\n\n{mensaje}'
            
            # Dirección de correo a la que se enviará el mensaje
            destinatario = settings.EMAIL_HOST_USER # O cualquier otra dirección

            # Enviar el correo
            send_mail(
                asunto,
                cuerpo,
                settings.EMAIL_HOST_USER, # Remitente
                [destinatario], # Lista de destinatarios
                fail_silently=False,
            )
            messages.add_message(request, messages.SUCCESS, "Email enviado correctamente.")
            return HttpResponseRedirect(reverse_lazy('home'))  # Redirige a una página de éxito
    else:
        form = ContactoForm()
    
    return render(request, "general/contact.html", {"form": form})


class DashboardView(TemplateView):
    template_name = 'general/dashboard.html'


@method_decorator(login_required, name='dispatch')
class CompanyDetailView(DetailView):
    template_name = 'general/companis/lista_companias.html'
    model = Company
    context_object_name = 'company'