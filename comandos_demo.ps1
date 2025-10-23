# 🔐 COMANDOS DE DEMOSTRACIÓN - LIBRERÍA E-COMMERCE
# Ejecutar en PowerShell desde el directorio del proyecto

# =====================================================
# 1. CONFIGURACIÓN INICIAL
# =====================================================

# Activar virtual environment (si no está activado)
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Crear migraciones y aplicar
python manage.py makemigrations
python manage.py migrate

# Crear usuarios de prueba
python manage.py create_test_users

# Crear libros de ejemplo
python manage.py create_sample_books

# =====================================================
# 2. EJECUTAR SERVIDOR
# =====================================================

# Iniciar servidor de desarrollo
python manage.py runserver

# El servidor estará disponible en: http://localhost:8000

# =====================================================
# 3. PRUEBAS DE API CON PowerShell
# =====================================================

# 3.1 REGISTRO DE USUARIO
$registerData = @{
    username = "testuser"
    email = "test@example.com"
    password = "TestPass123!"
    password_confirm = "TestPass123!"
    first_name = "Test"
    last_name = "User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $registerData

# 3.2 LOGIN Y OBTENER JWT
$loginData = @{
    email = "admin@libreria.com"
    password = "Admin123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $loginData

$token = $response.tokens.access
Write-Output "JWT Token: $token"

# 3.3 ACCESO AUTENTICADO
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/profile/" `
    -Method GET `
    -Headers $headers

# 3.4 LISTAR LIBROS (PÚBLICO)
Invoke-RestMethod -Uri "http://localhost:8000/api/books/" -Method GET

# 3.5 DASHBOARD ADMIN (SOLO ADMIN)
Invoke-RestMethod -Uri "http://localhost:8000/api/admin/dashboard/" `
    -Method GET `
    -Headers $headers

# 3.6 AGREGAR AL CARRITO
$cartData = @{
    libro_id = 1
    cantidad = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/cart/add/" `
    -Method POST `
    -Headers $headers `
    -Body $cartData

# 3.7 VER CARRITO
Invoke-RestMethod -Uri "http://localhost:8000/api/cart/" `
    -Method GET `
    -Headers $headers

# =====================================================
# 4. PRUEBAS DE SEGURIDAD
# =====================================================

# 4.1 PRUEBA DE RATE LIMITING (Hacer múltiples requests)
for ($i = 1; $i -le 15; $i++) {
    try {
        $result = Invoke-RestMethod -Uri "http://localhost:8000/api/books/" -Method GET
        Write-Output "Request $i: OK"
    }
    catch {
        Write-Output "Request $i: RATE LIMITED - $($_.Exception.Message)"
        break
    }
    Start-Sleep -Milliseconds 100
}

# 4.2 PRUEBA DE INYECCIÓN SQL (Será bloqueada)
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/books/?search='; DROP TABLE core_libro; --" -Method GET
}
catch {
    Write-Output "SQL Injection blocked: $($_.Exception.Message)"
}

# 4.3 PRUEBA DE XSS (Será bloqueada)
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/books/?search=<script>alert('xss')</script>" -Method GET
}
catch {
    Write-Output "XSS attempt blocked: $($_.Exception.Message)"
}

# 4.4 ACCESO SIN TOKEN (401)
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/admin/dashboard/" -Method GET
}
catch {
    Write-Output "Access denied without token: $($_.Exception.Message)"
}

# 4.5 TOKEN INVÁLIDO
$invalidHeaders = @{
    "Authorization" = "Bearer invalid_token_here"
    "Content-Type" = "application/json"
}

try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/auth/profile/" `
        -Method GET `
        -Headers $invalidHeaders
}
catch {
    Write-Output "Invalid token rejected: $($_.Exception.Message)"
}

# =====================================================
# 5. CREAR LIBRO (SOLO ADMIN/MODERATOR)
# =====================================================

$bookData = @{
    titulo = "Libro de Prueba PowerShell"
    descripcion = "Libro creado desde PowerShell"
    precio = 29.99
    stock = 10
    fecha_publicacion = "2024-01-01"
} | ConvertTo-Json

try {
    $newBook = Invoke-RestMethod -Uri "http://localhost:8000/api/books/create/" `
        -Method POST `
        -Headers $headers `
        -Body $bookData
    Write-Output "Libro creado: $($newBook.titulo)"
}
catch {
    Write-Output "Error creating book: $($_.Exception.Message)"
}

# =====================================================
# 6. PRUEBAS CON DIFERENTES USUARIOS
# =====================================================

# LOGIN COMO MODERADOR
$modLoginData = @{
    email = "moderator@libreria.com"
    password = "Mod123!"
} | ConvertTo-Json

$modResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $modLoginData

$modToken = $modResponse.tokens.access
$modHeaders = @{
    "Authorization" = "Bearer $modToken"
    "Content-Type" = "application/json"
}

# Moderador puede crear libros
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/books/create/" `
        -Method POST `
        -Headers $modHeaders `
        -Body $bookData
    Write-Output "Moderator can create books"
}
catch {
    Write-Output "Moderator cannot create books: $($_.Exception.Message)"
}

# Moderador NO puede acceder al dashboard admin
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/admin/dashboard/" `
        -Method GET `
        -Headers $modHeaders
}
catch {
    Write-Output "Moderator correctly denied admin access: $($_.Exception.Message)"
}

# LOGIN COMO USUARIO NORMAL
$userLoginData = @{
    email = "usuario@libreria.com"
    password = "User123!"
} | ConvertTo-Json

$userResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $userLoginData

$userToken = $userResponse.tokens.access
$userHeaders = @{
    "Authorization" = "Bearer $userToken"
    "Content-Type" = "application/json"
}

# Usuario puede ver su carrito
Invoke-RestMethod -Uri "http://localhost:8000/api/cart/" `
    -Method GET `
    -Headers $userHeaders

# Usuario NO puede crear libros
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/books/create/" `
        -Method POST `
        -Headers $userHeaders `
        -Body $bookData
}
catch {
    Write-Output "User correctly denied book creation: $($_.Exception.Message)"
}

# =====================================================
# 7. VERIFICAR LOGS DE SEGURIDAD
# =====================================================

# Ver últimas líneas del log de seguridad
Get-Content -Path "security.log" -Tail 20

# =====================================================
# 8. COMANDOS ÚTILES ADICIONALES
# =====================================================

# Ver estructura de la base de datos
python manage.py dbshell

# Crear superusuario interactivo
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ver todas las rutas
python manage.py show_urls

# Verificar configuración
python manage.py check

# Ejecutar tests
python manage.py test

# =====================================================
# 9. LIMPIAR Y REINICIAR
# =====================================================

# Eliminar base de datos y recrear
Remove-Item db.sqlite3 -Force
python manage.py migrate
python manage.py create_test_users
python manage.py create_sample_books

# =====================================================
# 10. EJEMPLOS DE RESPUESTAS ESPERADAS
# =====================================================

<#
REGISTRO EXITOSO:
{
  "message": "User registered successfully",
  "user": {
    "id": 5,
    "username": "testuser",
    "email": "test@example.com"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}

LOGIN EXITOSO:
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@libreria.com"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}

RATE LIMIT EXCEDIDO:
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Limit: 100 per 3600 seconds",
  "retry_after": 3600
}

ACCESO DENEGADO:
{
  "error": "Permission denied",
  "message": "Required permission: manage_users"
}

TOKEN INVÁLIDO:
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
#>

Write-Output "==================================================="
Write-Output "🎉 COMANDOS DE DEMOSTRACIÓN CARGADOS"
Write-Output "Ejecuta los comandos uno por uno para probar"
Write-Output "todas las funcionalidades de seguridad"
Write-Output "==================================================="