from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro, Carrito, ItemCarrito, UserProfile, Categoria, Autor, Editorial
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator
import logging

from .decorators import role_required, permission_required, validate_input, COMMON_VALIDATIONS

logger = logging.getLogger('security')

# Create your views here.

def home(request):
    # Obtener libros con paginación
    libros_list = Libro.objects.select_related('categoria', 'editorial').prefetch_related('autores').all()
    
    # Búsqueda segura
    search_query = request.GET.get('search', '')
    if search_query:
        # Validar la entrada de búsqueda
        import re
        if re.match(r'^[a-zA-Z0-9\s\-_.áéíóúñ]+$', search_query):
            libros_list = libros_list.filter(titulo__icontains=search_query)
        else:
            messages.warning(request, 'Término de búsqueda inválido.')
            logger.warning(f"Invalid search query from IP {get_client_ip(request)}: {search_query}")
    
    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id and categoria_id.isdigit():
        libros_list = libros_list.filter(categoria_id=categoria_id)
    
    # Paginación
    paginator = Paginator(libros_list.order_by('-id'), 12)  # 12 libros por página
    page_number = request.GET.get('page')
    libros = paginator.get_page(page_number)
    
    return render(request, 'pagCentral.html', {
        'libros': libros,
        'search_query': search_query
    })


def tienda(request):
    qs = Libro.objects.select_related('categoria', 'editorial').prefetch_related('autores').all()
    # filtros
    cat = request.GET.get('categoria')
    if cat and cat.isdigit():
        qs = qs.filter(categoria_id=int(cat))
    autor = request.GET.get('autor')
    if autor and autor.isdigit():
        qs = qs.filter(autores__id=int(autor))
    editorial = request.GET.get('editorial')
    if editorial and editorial.isdigit():
        qs = qs.filter(editorial_id=int(editorial))
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(titulo__icontains=q)

    paginator = Paginator(qs.distinct().order_by('-id'), 12)
    page = request.GET.get('page')
    libros = paginator.get_page(page)
    return render(request, 'tienda/listado.html', {
        'libros': libros,
        'categorias': Categoria.objects.all(),
        'autores': Autor.objects.all(),
        'editoriales': Editorial.objects.all(),
        'q': q,
    })


def categorias(request):
    return render(request, 'tienda/categorias.html', {
        'categorias': Categoria.objects.all()
    })


def categoria_detalle(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    libros = Libro.objects.filter(categoria=categoria).order_by('-id')
    paginator = Paginator(libros, 12)
    page = request.GET.get('page')
    return render(request, 'tienda/categoria_detalle.html', {
        'categoria': categoria,
        'libros': paginator.get_page(page)
    })


def autores(request):
    return render(request, 'tienda/autores.html', {
        'autores': Autor.objects.all()
    })


def autor_detalle(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    libros = Libro.objects.filter(autores=autor).order_by('-id')
    paginator = Paginator(libros, 12)
    page = request.GET.get('page')
    return render(request, 'tienda/autor_detalle.html', {
        'autor': autor,
        'libros': paginator.get_page(page)
    })


def editoriales(request):
    return render(request, 'tienda/editoriales.html', {
        'editoriales': Editorial.objects.all()
    })


def editorial_detalle(request, editorial_id):
    editorial = get_object_or_404(Editorial, id=editorial_id)
    libros = Libro.objects.filter(editorial=editorial).order_by('-id')
    paginator = Paginator(libros, 12)
    page = request.GET.get('page')
    return render(request, 'tienda/editorial_detalle.html', {
        'editorial': editorial,
        'libros': paginator.get_page(page)
    })


def nosotros(request):
    return render(request, 'static_pages/nosotros.html')


def contacto(request):
    if request.method == 'POST':
        messages.success(request, 'Gracias por contactarnos, te responderemos pronto.')
        return redirect('contacto')
    return render(request, 'static_pages/contacto.html')


def faq(request):
    return render(request, 'static_pages/faq.html')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    # Crear perfil de usuario por defecto
                    UserProfile.objects.create(user=user, role='USER')
                    
                    logger.info(f"New user registered: {user.username} from IP {get_client_ip(request)}")
                    messages.success(request, 'Usuario registrado exitosamente.')
                    return redirect('login')
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                messages.error(request, 'Error al registrar usuario.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/registro.html', {'form': form})


@login_required
@validate_input({
    'POST': {
        'cantidad': COMMON_VALIDATIONS['cantidad']
    }
})
def agregar_al_carrito(request, libro_id):
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('home')
    
    try:
        with transaction.atomic():
            libro = get_object_or_404(Libro, id=libro_id)
            
            # Verificar permisos del usuario
            profile = getattr(request.user, 'profile', None)
            if not profile:
                UserProfile.objects.create(user=request.user, role='USER')
                profile = request.user.profile
            
            if not profile.has_permission('manage_cart'):
                messages.error(request, 'No tienes permisos para agregar al carrito.')
                return redirect('home')
            
            # Busca o crea el carrito del usuario actual
            carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
            
            # Obtener la cantidad del formulario con validación
            cantidad_str = request.POST.get('cantidad', '1')
            try:
                cantidad = int(cantidad_str)
                if cantidad <= 0 or cantidad > 100:
                    raise ValueError("Cantidad inválida")
            except ValueError:
                messages.error(request, 'Cantidad inválida.')
                return redirect('libro_detail', libro_id=libro_id)
            
            # Verificar stock disponible
            if libro.stock < cantidad:
                messages.error(request, f'Stock insuficiente. Disponible: {libro.stock}')
                return redirect('libro_detail', libro_id=libro_id)
            
            # Busca si el libro ya está en el carrito
            item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, libro=libro)
            
            if not creado:
                # Verificar que la nueva cantidad total no exceda el stock
                nueva_cantidad = item.cantidad + cantidad
                if nueva_cantidad > libro.stock:
                    messages.error(request, f'Stock insuficiente. En carrito: {item.cantidad}, Disponible: {libro.stock}')
                    return redirect('libro_detail', libro_id=libro_id)
                item.cantidad = nueva_cantidad
            else:
                item.cantidad = cantidad
            
            item.save()
            
            logger.info(f"User {request.user.username} added {cantidad} of book {libro.titulo} to cart")
            messages.success(request, f'Se agregó "{libro.titulo}" al carrito.')
            
    except Exception as e:
        logger.error(f"Error adding to cart: {str(e)}")
        messages.error(request, 'Error al agregar al carrito.')
    
    return redirect('ver_carrito')


@login_required
@permission_required('manage_cart')
def ver_carrito(request):
    try:
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        items = carrito.items.select_related('libro__categoria', 'libro__editorial').all()
        total = sum(item.subtotal() for item in items)
        
        return render(request, 'carrito/ver_carrito.html', {
            'carrito': carrito,
            'items': items,
            'total': total,
        })
    except Exception as e:
        logger.error(f"Error viewing cart: {str(e)}")
        messages.error(request, 'Error al ver el carrito.')
        return redirect('home')


@login_required
@permission_required('manage_cart')
def eliminar_item(request, item_id):
    try:
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
        libro_titulo = item.libro.titulo
        item.delete()
        
        logger.info(f"User {request.user.username} removed {libro_titulo} from cart")
        messages.success(request, f'Se eliminó "{libro_titulo}" del carrito.')
    except Exception as e:
        logger.error(f"Error removing from cart: {str(e)}")
        messages.error(request, 'Error al eliminar del carrito.')
    
    return redirect('ver_carrito')


@validate_input({
    'GET': {
        'search': COMMON_VALIDATIONS['search']
    }
})
def libro_detail(request, libro_id):
    try:
        libro = get_object_or_404(Libro, id=libro_id)
        
        # Libros relacionados de la misma categoría (máximo 4)
        libros_relacionados = Libro.objects.filter(
            categoria=libro.categoria
        ).exclude(id=libro_id)[:4]
        
        return render(request, 'libros/libro_detail.html', {
            'libro': libro,
            'libros_relacionados': libros_relacionados
        })
    except Exception as e:
        logger.error(f"Error viewing book detail: {str(e)}")
        messages.error(request, 'Error al cargar el libro.')
        return redirect('home')


# Vista administrativa - solo para administradores
@login_required
@role_required(['ADMIN'])
def admin_dashboard(request):
    try:
        # Estadísticas básicas
        total_usuarios = User.objects.count()
        total_libros = Libro.objects.count()
        total_carritos = Carrito.objects.count()
        
        # Usuarios recientes
        usuarios_recientes = User.objects.order_by('-date_joined')[:5]
        
        return render(request, 'admin/dashboard.html', {
            'total_usuarios': total_usuarios,
            'total_libros': total_libros,
            'total_carritos': total_carritos,
            'usuarios_recientes': usuarios_recientes,
        })
    except Exception as e:
        logger.error(f"Error accessing admin dashboard: {str(e)}")
        messages.error(request, 'Error al acceder al panel administrativo.')
        return redirect('home')


# Vista de ejemplo que muestra diferentes datos según el rol
@login_required
def user_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        context = {
            'profile': profile,
            'user': request.user,
        }
        
        # Información adicional según el rol
        if profile.has_permission('view_all'):
            context['can_view_all'] = True
            context['total_users'] = User.objects.count()
        
        if profile.has_permission('manage_users'):
            context['can_manage_users'] = True
        
        return render(request, 'user/profile.html', context)
    except Exception as e:
        logger.error(f"Error viewing user profile: {str(e)}")
        messages.error(request, 'Error al cargar el perfil.')
        return redirect('home')


def get_client_ip(request):
    """Obtener la IP real del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def custom_404(request, exception):
    """Custom 404 handler rendering a friendly page"""
    return render(request, '404.html', status=404)


def debug_404(request):
    """Preview the 404 page while DEBUG=True"""
    return render(request, '404.html', status=404)

