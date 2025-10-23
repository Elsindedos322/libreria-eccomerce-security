from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Libro, Categoria, Editorial, Autor, Carrito, ItemCarrito, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
    
    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers and underscores.")
        return value
    
    def validate_password(self, value):
        # Validación de contraseña segura
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Crear perfil del usuario
        UserProfile.objects.create(user=user, role='USER')
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if not user:
                    raise serializers.ValidationError("Invalid credentials.")
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                attrs['user'] = user
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include email and password.")
        
        return attrs
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ('role', 'phone', 'address', 'date_of_birth', 'is_verified', 'user_info')
        read_only_fields = ('role', 'is_verified')
    
    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'date_joined': obj.user.date_joined,
            'is_active': obj.user.is_active
        }


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ('id', 'nombre', 'apellido')


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre')


class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ('id', 'nombre')


class LibroSerializer(serializers.ModelSerializer):
    autores = AutorSerializer(many=True, read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    editorial = EditorialSerializer(read_only=True)
    
    class Meta:
        model = Libro
        fields = ('id', 'titulo', 'descripcion', 'precio', 'stock', 'categoria', 
                 'editorial', 'autores', 'imagen', 'fecha_publicacion')
    
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class LibroCreateUpdateSerializer(serializers.ModelSerializer):
    autores_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    categoria_id = serializers.IntegerField(write_only=True, required=False)
    editorial_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Libro
        fields = ('titulo', 'descripcion', 'precio', 'stock', 'categoria_id',
                 'editorial_id', 'autores_ids', 'imagen', 'fecha_publicacion')
    
    def create(self, validated_data):
        autores_ids = validated_data.pop('autores_ids', [])
        categoria_id = validated_data.pop('categoria_id', None)
        editorial_id = validated_data.pop('editorial_id', None)
        
        if categoria_id:
            validated_data['categoria'] = Categoria.objects.get(id=categoria_id)
        if editorial_id:
            validated_data['editorial'] = Editorial.objects.get(id=editorial_id)
        
        libro = Libro.objects.create(**validated_data)
        
        if autores_ids:
            autores = Autor.objects.filter(id__in=autores_ids)
            libro.autores.set(autores)
        
        return libro


class ItemCarritoSerializer(serializers.ModelSerializer):
    libro = LibroSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = ItemCarrito
        fields = ('id', 'libro', 'cantidad', 'subtotal')


class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Carrito
        fields = ('id', 'items', 'total')


class AddToCartSerializer(serializers.Serializer):
    libro_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1, max_value=100)
    
    def validate_libro_id(self, value):
        try:
            Libro.objects.get(id=value)
        except Libro.DoesNotExist:
            raise serializers.ValidationError("Book not found.")
        return value
    
    def validate(self, attrs):
        libro = Libro.objects.get(id=attrs['libro_id'])
        if libro.stock < attrs['cantidad']:
            raise serializers.ValidationError(f"Not enough stock. Available: {libro.stock}")
        return attrs


# Serializer para respuestas que excluye campos sensibles
class SafeUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'profile')
        # Excluir campos sensibles como password