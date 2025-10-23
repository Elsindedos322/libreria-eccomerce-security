from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db import transaction
import logging

from .models import Libro, Carrito, ItemCarrito, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, LibroSerializer,
    CarritoSerializer, AddToCartSerializer, SafeUserSerializer,
    LibroCreateUpdateSerializer, UserProfileSerializer
)
from .decorators import role_required, permission_required, validate_input, COMMON_VALIDATIONS

logger = logging.getLogger('security')

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                logger.info(f"New user registered: {user.username} from IP {self.get_client_ip(request)}")
                
                return Response({
                    'message': 'User registered successfully',
                    'user': SafeUserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in user registration: {str(e)}")
            return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                tokens = serializer.get_tokens_for_user(user)
                
                logger.info(f"User login successful: {user.username} from IP {self.get_client_ip(request)}")
                
                return Response({
                    'message': 'Login successful',
                    'user': SafeUserSerializer(user).data,
                    'tokens': tokens
                }, status=status.HTTP_200_OK)
            
            # Log failed login attempt
            email = request.data.get('email', 'unknown')
            logger.warning(f"Failed login attempt for email {email} from IP {self.get_client_ip(request)}")
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in user login: {str(e)}")
            return Response({'error': 'Login failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            return Response({
                'user': SafeUserSerializer(request.user).data,
                'profile': UserProfileSerializer(profile).data
            })
        except Exception as e:
            logger.error(f"Error retrieving user profile: {str(e)}")
            return Response({'error': 'Failed to retrieve profile'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request):
        try:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Profile updated successfully', 'profile': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating user profile: {str(e)}")
            return Response({'error': 'Failed to update profile'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LibroListView(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [permissions.AllowAny]  # Permitir ver libros sin autenticación
    
    def get_queryset(self):
        queryset = Libro.objects.all()
        
        # Filtros de búsqueda seguros
        search = self.request.query_params.get('search', None)
        if search:
            # Validar entrada de búsqueda
            import re
            if re.match(r'^[a-zA-Z0-9\s\-_.áéíóúñ]+$', search):
                queryset = queryset.filter(titulo__icontains=search)
        
        categoria = self.request.query_params.get('categoria', None)
        if categoria and categoria.isdigit():
            queryset = queryset.filter(categoria_id=categoria)
        
        return queryset


class LibroDetailView(generics.RetrieveAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [permissions.AllowAny]


class LibroCreateView(generics.CreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Verificar permisos basados en roles
        profile = getattr(request.user, 'profile', None)
        if not profile or not profile.has_permission('create_books'):
            logger.warning(f"User {request.user.username} attempted to create book without permission")
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().create(request, *args, **kwargs)


class LibroUpdateView(generics.UpdateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        # Verificar permisos basados en roles
        profile = getattr(request.user, 'profile', None)
        if not profile or not profile.has_permission('edit_books'):
            logger.warning(f"User {request.user.username} attempted to update book without permission")
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)


class LibroDeleteView(generics.DestroyAPIView):
    queryset = Libro.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        # Verificar permisos basados en roles
        profile = getattr(request.user, 'profile', None)
        if not profile or not profile.has_permission('delete_books'):
            logger.warning(f"User {request.user.username} attempted to delete book without permission")
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)


class CarritoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            carrito, created = Carrito.objects.get_or_create(usuario=request.user)
            serializer = CarritoSerializer(carrito)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving cart: {str(e)}")
            return Response({'error': 'Failed to retrieve cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddToCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = AddToCartSerializer(data=request.data)
            if serializer.is_valid():
                libro_id = serializer.validated_data['libro_id']
                cantidad = serializer.validated_data['cantidad']
                
                with transaction.atomic():
                    libro = get_object_or_404(Libro, id=libro_id)
                    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
                    
                    # Verificar si el item ya existe en el carrito
                    item, item_created = ItemCarrito.objects.get_or_create(
                        carrito=carrito,
                        libro=libro,
                        defaults={'cantidad': cantidad}
                    )
                    
                    if not item_created:
                        item.cantidad += cantidad
                        item.save()
                    
                    logger.info(f"User {request.user.username} added {cantidad} of book {libro.titulo} to cart")
                    
                    return Response({
                        'message': 'Item added to cart successfully',
                        'cart': CarritoSerializer(carrito).data
                    }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error adding to cart: {str(e)}")
            return Response({'error': 'Failed to add to cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveFromCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, item_id):
        try:
            item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
            libro_titulo = item.libro.titulo
            item.delete()
            
            logger.info(f"User {request.user.username} removed {libro_titulo} from cart")
            
            return Response({'message': 'Item removed from cart successfully'})
        except Exception as e:
            logger.error(f"Error removing from cart: {str(e)}")
            return Response({'error': 'Failed to remove from cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_dashboard(request):
    """Vista de ejemplo que requiere permisos de administrador"""
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'ADMIN':
        logger.warning(f"Non-admin user {request.user.username} attempted to access admin dashboard")
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    # Datos del dashboard (ejemplo)
    total_users = User.objects.count()
    total_books = Libro.objects.count()
    
    return Response({
        'total_users': total_users,
        'total_books': total_books,
        'user_role': profile.role
    })


# Vista para demostrar filtrado de campos según rol
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    """Lista de usuarios con campos filtrados según el rol"""
    profile = getattr(request.user, 'profile', None)
    
    if not profile or not profile.has_permission('view_all'):
        # Usuario normal: solo puede ver información básica
        users = User.objects.filter(is_active=True).values('id', 'username', 'first_name', 'last_name')
    else:
        # Admin/Moderador: puede ver más información
        users = User.objects.all()
        users_data = []
        for user in users:
            user_data = SafeUserSerializer(user).data
            # Admins pueden ver emails y fechas
            if profile.role == 'ADMIN':
                user_data['email'] = user.email
                user_data['date_joined'] = user.date_joined
            users_data.append(user_data)
        return Response(users_data)
    
    return Response(list(users))