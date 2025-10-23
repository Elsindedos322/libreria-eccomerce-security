from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Extender el modelo User con roles
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('MODERATOR', 'Moderador'),
        ('USER', 'Usuario'),
        ('GUEST', 'Invitado'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def has_permission(self, permission):
        """Check if user has specific permission based on role"""
        permissions = {
            'ADMIN': ['view_all', 'edit_all', 'delete_all', 'create_all', 'manage_users'],
            'MODERATOR': ['view_all', 'edit_books', 'delete_books', 'create_books'],
            'USER': ['view_books', 'buy_books', 'manage_cart'],
            'GUEST': ['view_books'],
        }
        return permission in permissions.get(self.role, [])

# categorias

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
# editorial

class Editorial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
# autor

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
#libro

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="libros")
    editorial = models.ForeignKey(Editorial, on_delete=models.SET_NULL, null=True, related_name="libros")
    autores = models.ManyToManyField(Autor, related_name="libros")
    imagen = models.ImageField(upload_to="libros/", null=True, blank=True)
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo

#carrito

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.libro.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.libro.titulo}"

# pedido

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    direccion_envio = models.CharField(max_length=250)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.libro.titulo}"





