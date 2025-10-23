from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
import re
import logging

logger = logging.getLogger('security')

def role_required(allowed_roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles permitidos
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                user_profile = request.user.profile
                if user_profile.role not in allowed_roles:
                    logger.warning(f"Access denied for user {request.user.username} with role {user_profile.role} "
                                 f"to view requiring roles {allowed_roles}")
                    
                    if request.content_type == 'application/json':
                        return JsonResponse({
                            'error': 'Access denied',
                            'message': f'Required role: {" or ".join(allowed_roles)}'
                        }, status=403)
                    else:
                        messages.error(request, 'No tienes permisos para acceder a esta página.')
                        return redirect('home')
                
                return view_func(request, *args, **kwargs)
            except AttributeError:
                # Si el usuario no tiene perfil, crear uno por defecto
                from .models import UserProfile
                UserProfile.objects.create(user=request.user, role='USER')
                return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator


def permission_required(permission):
    """
    Decorador para verificar permisos específicos basados en roles
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                user_profile = request.user.profile
                if not user_profile.has_permission(permission):
                    logger.warning(f"Permission denied for user {request.user.username} "
                                 f"trying to access {permission}")
                    
                    if request.content_type == 'application/json':
                        return JsonResponse({
                            'error': 'Permission denied',
                            'message': f'Required permission: {permission}'
                        }, status=403)
                    else:
                        messages.error(request, 'No tienes permisos para realizar esta acción.')
                        return redirect('home')
                
                return view_func(request, *args, **kwargs)
            except AttributeError:
                from .models import UserProfile
                UserProfile.objects.create(user=request.user, role='USER')
                return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator


def validate_input(validation_rules):
    """
    Decorador para validar inputs y prevenir ataques de inyección
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Validar parámetros GET
            for param, rules in validation_rules.get('GET', {}).items():
                value = request.GET.get(param)
                if value and not _validate_value(value, rules):
                    logger.warning(f"Invalid GET parameter '{param}' with value '{value}' from user {request.user}")
                    return JsonResponse({
                        'error': 'Invalid input',
                        'message': f'Parameter {param} contains invalid characters'
                    }, status=400)
            
            # Validar parámetros POST para formularios
            if request.method == 'POST':
                for param, rules in validation_rules.get('POST', {}).items():
                    value = request.POST.get(param)
                    if value and not _validate_value(value, rules):
                        logger.warning(f"Invalid POST parameter '{param}' with value '{value}' from user {request.user}")
                        return JsonResponse({
                            'error': 'Invalid input',
                            'message': f'Parameter {param} contains invalid characters'
                        }, status=400)
            
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator


def _validate_value(value, rules):
    """
    Validar un valor según las reglas especificadas
    """
    # Verificar patrones maliciosos
    malicious_patterns = [
        r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>',  # Scripts
        r'javascript:',
        r'vbscript:',
        r'onload\s*=',
        r'onerror\s*=',
        r'union\s+select',  # SQL Injection
        r'drop\s+table',
        r'delete\s+from',
        r'insert\s+into',
        r'update\s+.*set',
        r'exec\s*\(',
        r'\.\.\/|\.\.\\',  # Path traversal
    ]
    
    for pattern in malicious_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            return False
    
    # Validaciones específicas
    if 'max_length' in rules and len(value) > rules['max_length']:
        return False
    
    if 'min_length' in rules and len(value) < rules['min_length']:
        return False
    
    if 'pattern' in rules and not re.match(rules['pattern'], value):
        return False
    
    if 'type' in rules:
        if rules['type'] == 'int':
            try:
                int(value)
            except ValueError:
                return False
        elif rules['type'] == 'float':
            try:
                float(value)
            except ValueError:
                return False
        elif rules['type'] == 'email':
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, value):
                return False
    
    return True


def sanitize_output(fields_to_exclude=None):
    """
    Decorador para sanitizar la salida y excluir campos sensibles
    """
    if fields_to_exclude is None:
        fields_to_exclude = ['password', 'secret_key', 'token']
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            
            # Si es una respuesta JSON, sanitizar los datos
            if hasattr(response, 'content') and response.get('Content-Type') == 'application/json':
                try:
                    import json
                    data = json.loads(response.content)
                    sanitized_data = _sanitize_dict(data, fields_to_exclude)
                    response.content = json.dumps(sanitized_data).encode()
                except (json.JSONDecodeError, AttributeError):
                    pass
            
            return response
        
        return _wrapped_view
    return decorator


def _sanitize_dict(data, fields_to_exclude):
    """
    Recursivamente remover campos sensibles de un diccionario
    """
    if isinstance(data, dict):
        return {
            key: _sanitize_dict(value, fields_to_exclude) 
            for key, value in data.items() 
            if key not in fields_to_exclude
        }
    elif isinstance(data, list):
        return [_sanitize_dict(item, fields_to_exclude) for item in data]
    else:
        return data


# Validaciones específicas comunes
COMMON_VALIDATIONS = {
    'libro_id': {
        'type': 'int',
        'min_length': 1,
        'max_length': 10
    },
    'cantidad': {
        'type': 'int',
        'min_length': 1,
        'max_length': 3,
        'pattern': r'^[1-9]\d*$'  # Solo números positivos
    },
    'search': {
        'max_length': 100,
        'pattern': r'^[a-zA-Z0-9\s\-_.áéíóúñ]+$'  # Solo caracteres alfanuméricos y básicos
    },
    'email': {
        'type': 'email',
        'max_length': 254
    }
}