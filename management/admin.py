from django.contrib import admin
from .models import Company, Client, Interaction

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cif', 'email', 'phone', 'created_at')
    search_fields = ('name', 'cif')
    list_filter = ('created_at',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'get_commercials', 'email')
    # Campos por los que se puede buscar 
    search_fields = ('first_name', 'last_name', 'email', 'company__name') # Búsqueda por nombre de empresa
    # Filtros laterales
    list_filter = ('company', 'assigned_commercials') 
    # Para mostrar la relación ManyToMany de forma más amigable
    filter_horizontal = ('assigned_commercials',)
    
    # Campo personalizado para mostrar los comerciales asignados en el listado
    def get_commercials(self, obj):
        return ", ".join([user.username for user in obj.assigned_commercials.all()])
    get_commercials.short_description = 'Comerciales'


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('client', 'type', 'commercial', 'interaction_date', 'created_at')
    
    # Filtros laterales
    list_filter = ('type', 'commercial', 'interaction_date')
    
    # Campos por los que se puede buscar
    search_fields = ('client__first_name', 'client__last_name', 'notes')
    
    # Campos que se muestran al editar un registro
    fields = ('client', 'commercial', 'type', 'interaction_date', 'notes')