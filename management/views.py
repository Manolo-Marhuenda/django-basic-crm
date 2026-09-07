from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages 
from .models import Client, Company
from .forms import ClientForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ClienteCreateView(CreateView):
    template_name = 'general/client/crear_cliente.html'
    model = Client
    form_class= ClientForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Cliente creado correctamente.")
        return super(ClienteCreateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class ClientDetailView(DetailView):
    template_name = 'general/client/detail_cliente.html'
    model = Client
    context_object_name = 'client'

@method_decorator(login_required, name='dispatch')
class CompanyDetailView(DetailView):
    template_name = 'general/companis/detail_companias.html'
    model = Company
    context_object_name = 'company'

    
class CompanyListView(ListView):
    model = Company
    template_name = 'general/companis/lista_companias.html'
    context_object_name = 'companies'


# class CompanyUpdateView(LoginRequiredMixin, UpdateView):
#     model = Company
#     form_class = CompanyForm
#     template_name = 'general/companis/editar_compania.html'
#     success_url = reverse_lazy('company_list')

#     def form_valid(self, form):
#         messages.add_message(self.request, messages.SUCCESS, "Cliente actualizado correctamente.")
#         return super().form_valid(form)