"""
URL configuration for libreria project.

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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('core.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    
    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Servir archivos media y estáticos correctamente según DEBUG
if settings.DEBUG:
    # En desarrollo, Django sirve estáticos desde los finders (STATICFILES_DIRS, apps)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Con DEBUG=False, agregar un mapeo explícito para /static/ y /media/ usando django.views.static.serve
    # Nota: Esto es solo para uso local con runserver; en producción debe servirse con un servidor web.
    if getattr(settings, 'STATIC_ROOT', None):
        urlpatterns += [
            re_path(r'^static/(?P<path>.*)$', static_serve, {'document_root': settings.STATIC_ROOT}),
        ]
    if getattr(settings, 'MEDIA_ROOT', None):
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
        ]

handler404 = 'core.views.custom_404'
