"""
URL configuration for crm_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crm_project.views import HomeView, LoginView, RegisterView, LegalView, logout_view, contacto, DashboardView
from management.views import ClienteDeleteView, ClienteUpdateView, CompanyListView, CompanyDetailView, ClienteCreateView, ClientDetailView, InteractionCreateView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', contacto, name='contact'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('Company/', CompanyListView.as_view(), name='lista_companias'),
    path('Company/<int:pk>/', CompanyDetailView.as_view(), name='detail_companias'),
    path('Client/create/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('Client/<int:pk>/', ClientDetailView.as_view(), name='detail_cliente'),
    path('Client/<int:pk>/edit/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('Client/<int:pk>/delete/', ClienteDeleteView.as_view(), name='delete_client'),
    path('Interaction/create/<int:client_id>/', InteractionCreateView.as_view(), name='crear_interaccion'),
    # path('Company/<int:pk>/edit/', CompanyUpdateView.as_view(), name='editar_compania'),
    path('legal/', LegalView.as_view(), name='legal'),
    path('admin/', admin.site.urls),
]
