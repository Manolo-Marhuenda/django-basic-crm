from django.shortcuts import render
from django.views.generic import DeleteView, TemplateView, FormView, CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.contrib import messages 
from .models import Client, Company, Interaction
from .forms import ClientCreateForm, ClientUpdateForm, InteractionForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ClienteCreateView(CreateView):
    template_name = 'general/client/crear_cliente.html'
    model = Client
    form_class= ClientCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # 1. Guarda el cliente primero en la base de datos
        response = super().form_valid(form)
        
        # 2. Asigna al usuario actual como comercial en la relación ManyToMany
        self.object.assigned_commercials.add(self.request.user)
        
        # 3. Añade el mensaje de éxito
        messages.success(self.request, "Cliente creado correctamente.")
        
        return response


class ClienteUpdateView(UpdateView):
    template_name = 'general/client/editar_cliente.html'
    model = Client
    form_class= ClientUpdateForm

        #para ir a la vista de detalle del cliente después de actualizarlo
    def get_success_url(self):
        # Usamos reverse() pasando el pk del objeto recién guardado
        return reverse('detail_cliente', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Cliente actualizado correctamente.")
        return response


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    
    success_url = reverse_lazy('lista_companias')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Cliente eliminado correctamente.")
        return super().post(request, *args, **kwargs)

    # Si se accede por GET (clic en un enlace normal), realiza el borrado directo sin pedir plantilla
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ClientDetailView(DetailView):
    template_name = 'general/client/detail_cliente.html'
    model = Client
    context_object_name = 'client'
    #para pasar el formulario de interacción al template y funcione el modal.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_form'] = InteractionForm()
        return context

@method_decorator(login_required, name='dispatch')
class CompanyDetailView(DetailView):
    template_name = 'general/companis/detail_companias.html'
    model = Company
    context_object_name = 'company'

    
class CompanyListView(ListView):
    model = Company
    template_name = 'general/companis/lista_companias.html'
    context_object_name = 'companies'


class InteractionCreateView(LoginRequiredMixin, CreateView):
    model = Interaction
    form_class = InteractionForm

    def form_valid(self, form):
        # Asigna la clave primaria del cliente directamente desde la URL
        form.instance.client_id = self.kwargs['client_id']
        
        # Asigna el usuario actual como el comercial
        form.instance.commercial = self.request.user

        messages.success(self.request, "Interacción registrada correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige de vuelta al detalle del cliente recién actualizado
        return reverse('detail_cliente', kwargs={'pk': self.kwargs['client_id']})


class InteractionDeleteView(LoginRequiredMixin, DeleteView):
    model = Interaction

    def get_success_url(self):
        # Redirige de vuelta al detalle del cliente después de eliminar la interacción
        return reverse('detail_cliente', kwargs={'pk': self.object.client.pk})

    def post(self, request, *args, **kwargs):
        messages.success(request, "Interacción eliminada correctamente.")
        return super().post(request, *args, **kwargs)


class InteractionUpdateView(LoginRequiredMixin, UpdateView): 
    model = Interaction
    form_class = InteractionForm
    template_name = 'general/interaccion/editar_interaccion.html'

    def get_success_url(self):
        # Redirige de vuelta al detalle del cliente después de actualizar la interacción
        return reverse('detail_cliente', kwargs={'pk': self.object.client.pk})

    def form_valid(self, form):
        messages.success(self.request, "Interacción actualizada correctamente.")
        return super().form_valid(form)