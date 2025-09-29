from django.db import models
from django.contrib.auth.models import User
from .validators import validate_cif

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    cif = models.CharField(max_length=20, unique=True, verbose_name='CIF', validators=[validate_cif])
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    
    class Meta:
        verbose_name_plural = "Companies"
        
    def __str__(self):
        return self.name
    

class Client(models.Model):
    # --- Datos de Contacto (Sin cambios) ---
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    

    # Un cliente tiene VARIOS comerciales; un comercial tiene VARIOS clientes.
    assigned_commercials = models.ManyToManyField(
        User, 
        related_name='clients',
        verbose_name='Comerciales Asignados',
        # Opcional: Filtra para mostrar solo los usuarios que son comerciales.
        limit_choices_to={'is_staff': True} 
    )
    
    # Una empresa tiene VARIOS clientes; un cliente tiene SOLO UNA empresa.
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='contacts',
        verbose_name='Empresa'
    )
    
    # --- Datos de Control ---
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company.name})"
    

INTERACTION_CHOICES = (
    ('LLAMADA', 'Llamada Telefónica'),
    ('EMAIL', 'Correo Electrónico'),
    ('REUNION', 'Reunión Presencial/Virtual'),
    ('OTRO', 'Otro'),
)


class Interaction(models.Model):
    # --- Relaciones ---
    # La interacción está relacionada con UN cliente (Muchos a Uno: M:1)
    client = models.ForeignKey(
        'Client', # Usamos el string 'Client' porque el modelo ya está definido en este archivo.
        on_delete=models.CASCADE, # Si el cliente se borra, también se borran sus interacciones.
        related_name='interactions',
        verbose_name='Cliente'
    )
    
    # La interacción fue realizada por UN comercial (Muchos a Uno: M:1)
    commercial = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, # Si el comercial se borra, se mantiene la interacción con campo vacío.
        null=True,
        verbose_name='Comercial'
    )
    
    # --- Datos de la Interacción ---
    # Tipo de interacción (usamos las opciones definidas arriba)
    type = models.CharField(
        max_length=10,
        choices=INTERACTION_CHOICES,
        default='LLAMADA',
        verbose_name='Tipo de Interacción'
    )
    
    # Descripción/Detalle de la actividad
    notes = models.TextField(verbose_name='Notas / Resumen')
    
    # Fecha y hora en la que ocurrió la interacción
    interaction_date = models.DateField(verbose_name='Fecha y Hora')
    
    # --- Datos de Control ---
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Interacción"
        verbose_name_plural = "Interacciones"
        ordering = ['-interaction_date'] # Muestra las más recientes primero

    def __str__(self):
        return f"{self.type} con {self.client.first_name} el {self.interaction_date.strftime('%Y-%m-%d')}"