from django.urls import path, include
from . import views, api_views
from rest_framework.routers import DefaultRouter

# API URLs
api_urlpatterns = [
    # Authentication
    path('auth/register/', api_views.UserRegistrationView.as_view(), name='api_register'),
    path('auth/login/', api_views.UserLoginView.as_view(), name='api_login'),
    path('auth/profile/', api_views.UserProfileView.as_view(), name='api_profile'),
    
    # Books
    path('books/', api_views.LibroListView.as_view(), name='api_books_list'),
    path('books/<int:pk>/', api_views.LibroDetailView.as_view(), name='api_book_detail'),
    path('books/create/', api_views.LibroCreateView.as_view(), name='api_book_create'),
    path('books/<int:pk>/update/', api_views.LibroUpdateView.as_view(), name='api_book_update'),
    path('books/<int:pk>/delete/', api_views.LibroDeleteView.as_view(), name='api_book_delete'),
    
    # Cart
    path('cart/', api_views.CarritoView.as_view(), name='api_cart'),
    path('cart/add/', api_views.AddToCartView.as_view(), name='api_cart_add'),
    path('cart/remove/<int:item_id>/', api_views.RemoveFromCartView.as_view(), name='api_cart_remove'),
    
    # Admin
    path('admin/dashboard/', api_views.admin_dashboard, name='api_admin_dashboard'),
    path('admin/users/', api_views.user_list, name='api_user_list'),
]

urlpatterns = [
    # Web views
    path('', views.home, name='home'),
    path('tienda/', views.tienda, name='tienda'),
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/<int:categoria_id>/', views.categoria_detalle, name='categoria_detalle'),
    path('autores/', views.autores, name='autores'),
    path('autores/<int:autor_id>/', views.autor_detalle, name='autor_detalle'),
    path('editoriales/', views.editoriales, name='editoriales'),
    path('editoriales/<int:editorial_id>/', views.editorial_detalle, name='editorial_detalle'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('faq/', views.faq, name='faq'),
    path('registro/', views.registro, name='registro'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('libros/<int:libro_id>/', views.libro_detail, name='libro_detail'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('perfil/', views.user_profile, name='user_profile'),
    
    # Preview 404 page while DEBUG=True
    path('debug-404/', views.debug_404, name='debug_404'),
    
    # API
    path('api/', include(api_urlpatterns)),
]
