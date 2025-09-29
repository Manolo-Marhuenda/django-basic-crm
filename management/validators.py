import re
from django.core.exceptions import ValidationError

def validate_cif(value):
    """
    Valida la estructura básica de un NIF/CIF.
    (Simplificado para el ejercicio, pero comprueba la longitud y patrón).
    """
    value = value.upper() # Convertir a mayúsculas
    
    # 1. Comprueba la longitud (8 números + 1 letra/número)
    if len(value) != 9:
        raise ValidationError('El CIF debe tener 9 caracteres.')

    # 2. Comprueba el patrón básico (Letra/Número, 7 dígitos, Letra/Número)
    # Patrón: LNNNNNNNL (donde L es Letra y N es Número)
    if not re.match(r'^[A-HJNPQRSUVWZ]\d{7}[0-9A-J]$|^[XYZ]\d{7}[A-Z]$|^\d{8}[A-Z]$', value):
        raise ValidationError('El formato del CIF no es válido.')

    # NOTA: La lógica para validar el dígito de control real es compleja y extensa.
    # Si quieremos una validación completa, tendrías que importar una librería externa (como 'cifvalidator').
    
    return value