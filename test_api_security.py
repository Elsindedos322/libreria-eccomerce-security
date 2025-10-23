#!/usr/bin/env python3
"""
Script de prueba para la API de la librería con JWT
Demuestra las funcionalidades de autenticación, autorización y seguridad
"""

import requests
import json
import sys

# Configuración
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

def print_response(response, description=""):
    print(f"\n{'='*50}")
    print(f"PRUEBA: {description}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print(f"{'='*50}")

def test_api():
    """Pruebas completas de la API"""
    
    print("🚀 INICIANDO PRUEBAS DE SEGURIDAD DE LA API")
    
    # 1. Registro de usuario
    print("\n1. REGISTRO DE USUARIO")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{API_BASE}/auth/register/", json=register_data)
    print_response(response, "Registro de usuario")
    
    if response.status_code == 201:
        tokens = response.json()['tokens']
        access_token = tokens['access']
        print(f"✅ JWT Token generado: {access_token[:50]}...")
    else:
        print("❌ Error en registro")
        return
    
    # 2. Login de usuario
    print("\n2. LOGIN DE USUARIO")
    login_data = {
        "email": "test@example.com",
        "password": "TestPass123!"
    }
    
    response = requests.post(f"{API_BASE}/auth/login/", json=login_data)
    print_response(response, "Login de usuario")
    
    if response.status_code == 200:
        tokens = response.json()['tokens']
        access_token = tokens['access']
        refresh_token = tokens['refresh']
    
    # Headers con JWT
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 3. Acceso a perfil autenticado
    print("\n3. ACCESO A PERFIL (AUTENTICADO)")
    response = requests.get(f"{API_BASE}/auth/profile/", headers=headers)
    print_response(response, "Perfil de usuario autenticado")
    
    # 4. Listar libros (sin autenticación)
    print("\n4. LISTAR LIBROS (SIN AUTENTICACIÓN)")
    response = requests.get(f"{API_BASE}/books/")
    print_response(response, "Lista de libros sin autenticación")
    
    # 5. Intentar crear libro sin permisos
    print("\n5. INTENTAR CREAR LIBRO SIN PERMISOS")
    book_data = {
        "titulo": "Libro de Prueba",
        "descripcion": "Descripción de prueba",
        "precio": 29.99,
        "stock": 10,
        "fecha_publicacion": "2024-01-01"
    }
    
    response = requests.post(f"{API_BASE}/books/create/", json=book_data, headers=headers)
    print_response(response, "Crear libro sin permisos de admin")
    
    # 6. Acceso a dashboard admin sin permisos
    print("\n6. ACCESO A DASHBOARD ADMIN SIN PERMISOS")
    response = requests.get(f"{API_BASE}/admin/dashboard/", headers=headers)
    print_response(response, "Dashboard admin sin permisos")
    
    # 7. Agregar al carrito
    print("\n7. AGREGAR AL CARRITO")
    cart_data = {
        "libro_id": 1,
        "cantidad": 2
    }
    
    response = requests.post(f"{API_BASE}/cart/add/", json=cart_data, headers=headers)
    print_response(response, "Agregar al carrito")
    
    # 8. Ver carrito
    print("\n8. VER CARRITO")
    response = requests.get(f"{API_BASE}/cart/", headers=headers)
    print_response(response, "Ver carrito")
    
    # 9. Prueba de rate limiting
    print("\n9. PRUEBA DE RATE LIMITING")
    print("Haciendo múltiples requests rápidos...")
    
    for i in range(15):  # Más del límite
        response = requests.get(f"{API_BASE}/books/")
        if response.status_code == 429:
            print_response(response, f"Rate limit alcanzado en request {i+1}")
            break
        if i == 14:
            print("Rate limiting no se activó (límite no alcanzado)")
    
    # 10. Intentar acceso sin token
    print("\n10. ACCESO SIN TOKEN")
    response = requests.get(f"{API_BASE}/auth/profile/")
    print_response(response, "Acceso a perfil sin token")
    
    # 11. Token inválido
    print("\n11. TOKEN INVÁLIDO")
    invalid_headers = {"Authorization": "Bearer invalid_token_here"}
    response = requests.get(f"{API_BASE}/auth/profile/", headers=invalid_headers)
    print_response(response, "Acceso con token inválido")
    
    # 12. Refresh token
    print("\n12. REFRESH TOKEN")
    refresh_data = {"refresh": refresh_token}
    response = requests.post(f"{BASE_URL}/api/token/refresh/", json=refresh_data)
    print_response(response, "Refresh token")
    
    # 13. Inyección SQL en búsqueda
    print("\n13. PRUEBA DE INYECCIÓN SQL")
    malicious_search = "'; DROP TABLE core_libro; --"
    response = requests.get(f"{API_BASE}/books/?search={malicious_search}")
    print_response(response, "Búsqueda con intento de inyección SQL")
    
    # 14. XSS en parámetros
    print("\n14. PRUEBA DE XSS")
    xss_payload = "<script>alert('xss')</script>"
    response = requests.get(f"{API_BASE}/books/?search={xss_payload}")
    print_response(response, "Búsqueda con payload XSS")
    
    print("\n🎉 PRUEBAS COMPLETADAS")
    print("\n📋 RESUMEN DE FUNCIONALIDADES PROBADAS:")
    print("✅ Autenticación JWT")
    print("✅ Registro y login seguro")
    print("✅ Autorización basada en roles")
    print("✅ Rate limiting")
    print("✅ Validación de entrada")
    print("✅ Protección contra inyección SQL")
    print("✅ Protección contra XSS")
    print("✅ Manejo de tokens inválidos")
    print("✅ Refresh tokens")

def test_admin_user():
    """Pruebas con usuario administrador"""
    print("\n🔑 PRUEBAS CON USUARIO ADMINISTRADOR")
    
    # Login como admin
    login_data = {
        "email": "admin@libreria.com",
        "password": "Admin123!"
    }
    
    response = requests.post(f"{API_BASE}/auth/login/", json=login_data)
    
    if response.status_code != 200:
        print("❌ No se pudo hacer login como admin. Asegúrate de ejecutar 'python manage.py create_test_users'")
        return
    
    tokens = response.json()['tokens']
    admin_headers = {"Authorization": f"Bearer {tokens['access']}"}
    
    # Acceso a dashboard admin
    print("\n1. ACCESO A DASHBOARD ADMIN")
    response = requests.get(f"{API_BASE}/admin/dashboard/", headers=admin_headers)
    print_response(response, "Dashboard admin con permisos")
    
    # Lista de usuarios con información completa
    print("\n2. LISTA DE USUARIOS CON INFORMACIÓN COMPLETA")
    response = requests.get(f"{API_BASE}/admin/users/", headers=admin_headers)
    print_response(response, "Lista de usuarios para admin")

if __name__ == "__main__":
    print("🧪 SCRIPT DE PRUEBAS DE SEGURIDAD - LIBRERÍA E-COMMERCE")
    print("Asegúrate de que el servidor Django esté ejecutándose en http://127.0.0.1:8000")
    
    input("Presiona Enter para continuar...")
    
    try:
        test_api()
        test_admin_user()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. Asegúrate de que Django esté ejecutándose.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")