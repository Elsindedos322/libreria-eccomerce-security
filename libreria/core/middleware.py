import logging
import time
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
import json

logger = logging.getLogger('security')

class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware para implementar rate limiting y prevenir ataques de fuerza bruta
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
        
    def process_request(self, request):
        if not getattr(settings, 'RATELIMIT_ENABLE', True):
            return None
            
        # Obtener IP del cliente
        client_ip = self.get_client_ip(request)
        
        # Diferentes límites para diferentes endpoints
        if request.path.startswith('/admin/'):
            return self.check_rate_limit(request, client_ip, 'admin', limit=10, window=300)  # 10 requests per 5 min
        elif request.path.startswith('/api/auth/'):
            return self.check_rate_limit(request, client_ip, 'auth', limit=5, window=300)   # 5 requests per 5 min
        elif request.path.startswith('/api/'):
            return self.check_rate_limit(request, client_ip, 'api', limit=100, window=3600) # 100 requests per hour
        else:
            return self.check_rate_limit(request, client_ip, 'general', limit=200, window=3600) # 200 requests per hour
    
    def get_client_ip(self, request):
        """Obtener la IP real del cliente considerando proxies"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_rate_limit(self, request, client_ip, endpoint_type, limit, window):
        """Verificar si se ha excedido el rate limit"""
        cache_key = f"rate_limit:{endpoint_type}:{client_ip}"
        
        # Obtener contador actual
        current_count = cache.get(cache_key, 0)
        
        if current_count >= limit:
            # Log del intento de rate limiting
            logger.warning(f"Rate limit exceeded for IP {client_ip} on {endpoint_type} endpoint. "
                         f"Count: {current_count}, Limit: {limit}")
            
            # Respuesta de error
            response = JsonResponse({
                'error': 'Rate limit exceeded',
                'message': f'Too many requests. Limit: {limit} per {window} seconds',
                'retry_after': window
            })
            response.status_code = 429
            return response
        
        # Incrementar contador
        cache.set(cache_key, current_count + 1, window)
        
        return None


class SecurityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware para logging de eventos de seguridad
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        # Log de intentos de acceso sospechosos
        self.log_suspicious_activity(request)
        return None
    
    def process_response(self, request, response):
        # Log de respuestas de error de autenticación
        if response.status_code in [401, 403]:
            self.log_auth_failure(request, response)
        return response
    
    def log_suspicious_activity(self, request):
        """Log de actividad sospechosa"""
        suspicious_patterns = [
            'DROP TABLE', 'UNION SELECT', 'SCRIPT>', '<IFRAME',
            '../', '..\\', 'eval(', 'javascript:',
            'passwd', '/etc/', 'cmd.exe', 'powershell'
        ]
        
        # Verificar en parámetros GET
        query_string = request.GET.urlencode()
        for pattern in suspicious_patterns:
            if pattern.lower() in query_string.lower():
                logger.warning(f"Suspicious GET parameter detected from IP {self.get_client_ip(request)}: "
                             f"Pattern '{pattern}' in '{query_string[:200]}'")
                break
        
        # Verificar en el user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        suspicious_agents = ['sqlmap', 'nikto', 'nmap', 'burp', 'dirb']
        for agent in suspicious_agents:
            if agent.lower() in user_agent.lower():
                logger.warning(f"Suspicious User-Agent detected from IP {self.get_client_ip(request)}: {user_agent}")
                break
    
    def log_auth_failure(self, request, response):
        """Log de fallos de autenticación"""
        client_ip = self.get_client_ip(request)
        user = getattr(request, 'user', None)
        username = user.username if user and not isinstance(user, AnonymousUser) else 'Anonymous'
        
        logger.info(f"Authentication failure - IP: {client_ip}, User: {username}, "
                   f"Path: {request.path}, Status: {response.status_code}")
    
    def get_client_ip(self, request):
        """Obtener la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class XSSProtectionMiddleware(MiddlewareMixin):
    """
    Middleware adicional de protección XSS
    """
    
    def process_response(self, request, response):
        # Agregar headers de seguridad adicionales
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        return response