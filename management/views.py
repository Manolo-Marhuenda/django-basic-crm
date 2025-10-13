from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages 
from .models import Company
from .forms import CompanyForm 

# Create your views here.
@method_decorator(login_required, name='dispatch')
class CompanyCreateView(CreateView):
    template_name = 'general/companis/crear_compania.html'
    model = Company
    form_class= CompanyForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Compañia creada correctamente.")
        return super(CompanyCreateView, self).form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class CompanyDetailView(DetailView, CreateView):
    template_name = 'general/companis/lista_companias.html'
    model = Company
    form_class= CompanyForm
    context_object_name = 'company'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.reloj = self.get_object()
        return super(CompanyDetailView, self).form_valid(form)
    
class CompanyListView(ListView):
    # 1. Especifica el modelo que quieres listar
    model = Company
    
    # 2. Especifica el nombre del template a usar
    template_name = 'general/companis/lista_companias.html'
    
    # 3. Opcional: Nombre de la variable de contexto que contendrá la lista
    # Por defecto es 'object_list', pero 'companies' es más claro.
    context_object_name = 'companies'