# 🔐 Librería E-commerce con Seguridad Avanzada

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema de e-commerce para una librería con características avanzadas de seguridad, incluyendo:

- **JWT (JSON Web Tokens)** para autenticación segura
- **OAuth2** con Google para autenticación externa
- **Sistema de roles y permisos** (Admin, Moderador, Usuario, Invitado)
- **Rate limiting** para prevenir ataques de fuerza bruta
- **Validaciones de entrada** para prevenir inyecciones
- **CORS** configurado correctamente
- **Logging de seguridad** para auditoría

## 🚀 Funcionalidades de Seguridad Implementadas

### 1. Autenticación JWT
- ✅ Tokens de acceso y refresh
- ✅ Expiración automática de tokens
- ✅ Renovación segura de tokens
- ✅ Invalidación de tokens en logout

### 2. Sistema de Roles y Permisos
- **ADMIN**: Acceso completo al sistema
- **MODERATOR**: Gestión de libros y contenido
- **USER**: Compra de libros y gestión de carrito
- **GUEST**: Solo visualización de libros

### 3. Seguridad en Peticiones
- ✅ Rate limiting por IP y endpoint
- ✅ Validación de entrada contra XSS e inyección SQL
- ✅ Headers de seguridad (HSTS, XSS Protection, etc.)
- ✅ CORS configurado para desarrollo y producción

### 4. Validaciones y Filtrado
- ✅ Sanitización de inputs del usuario
- ✅ Filtrado de campos sensibles en respuestas API
- ✅ Validación de tipos de datos y longitudes
- ✅ Protección contra path traversal

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Django 5.2+
- Virtual Environment

### 1. Configurar el entorno
```bash
# Crear y activar virtual environment
python -m venv .venv
.venv\\Scripts\\activate  # En Windows
source .venv/bin/activate  # En Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
GOOGLE_OAUTH2_CLIENT_ID=tu_google_client_id
GOOGLE_OAUTH2_CLIENT_SECRET=tu_google_client_secret
```

### 3. Configurar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear datos de prueba
```bash
# Crear usuarios con diferentes roles
python manage.py create_test_users

# Crear libros de ejemplo
python manage.py create_sample_books
```

### 5. Ejecutar servidor
```bash
python manage.py runserver
```

## 🔑 Usuarios de Prueba

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| admin | Admin123! | ADMIN | Acceso completo |
| moderator | Mod123! | MODERATOR | Gestión de libros |
| usuario | User123! | USER | Compras y carrito |
| invitado | Guest123! | GUEST | Solo visualización |

## 🌐 Endpoints de la API

### Autenticación
```http
POST /api/auth/register/     # Registro de usuario
POST /api/auth/login/        # Login con JWT
GET  /api/auth/profile/      # Perfil del usuario
POST /api/token/             # Obtener token JWT
POST /api/token/refresh/     # Renovar token
```

### Libros
```http
GET    /api/books/           # Listar libros (público)
GET    /api/books/{id}/      # Detalle de libro
POST   /api/books/create/    # Crear libro (Admin/Mod)
PUT    /api/books/{id}/update/ # Actualizar libro (Admin/Mod)
DELETE /api/books/{id}/delete/ # Eliminar libro (Admin/Mod)
```

### Carrito
```http
GET  /api/cart/              # Ver carrito
POST /api/cart/add/          # Agregar al carrito
DELETE /api/cart/remove/{id}/ # Eliminar del carrito
```

### Administración
```http
GET /api/admin/dashboard/    # Dashboard admin (Solo Admin)
GET /api/admin/users/        # Lista de usuarios (Solo Admin)
```

## 🧪 Pruebas de Seguridad

### Ejecutar script de pruebas
```bash
python test_api_security.py
```

Este script prueba:
- ✅ Autenticación JWT
- ✅ Autorización por roles
- ✅ Rate limiting
- ✅ Validación de entrada
- ✅ Protección contra inyecciones
- ✅ Manejo de tokens inválidos

### Ejemplos de uso con curl

#### 1. Registro de usuario
```bash
curl -X POST http://localhost:8000/api/auth/register/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

#### 2. Login y obtener JWT
```bash
curl -X POST http://localhost:8000/api/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

#### 3. Acceso autenticado
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### 4. Prueba de rate limiting
```bash
# Hacer múltiples requests rápidamente
for i in {1..20}; do
  curl http://localhost:8000/api/books/
done
```

## 🔒 Características de Seguridad Detalladas

### Rate Limiting
- **Admin endpoints**: 10 requests/5min
- **Auth endpoints**: 5 requests/5min  
- **API general**: 100 requests/hora
- **Web general**: 200 requests/hora

### Validaciones de Entrada
- **SQL Injection**: Protección contra UNION, DROP, etc.
- **XSS**: Filtrado de scripts y eventos JavaScript
- **Path Traversal**: Bloqueo de ../ y ../
- **Longitud**: Límites en campos de texto
- **Tipo de datos**: Validación estricta de tipos

### Headers de Seguridad
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Referrer-Policy: strict-origin-when-cross-origin
```

### Logging de Seguridad
```python
# Logs en security.log
- Intentos de login fallidos
- Accesos denegados por permisos
- Rate limiting activado
- Intentos de inyección detectados
- Patrones de User-Agent sospechosos
```

## 📊 Dashboard y Visualización

### Panel de Administrador
- **URL**: `/admin/dashboard/`
- **Requiere**: Rol ADMIN
- **Muestra**: Estadísticas, usuarios recientes, logs de seguridad

### Perfil de Usuario
- **URL**: `/perfil/`
- **Muestra**: Permisos según rol, pruebas de API interactivas

## 🚀 Despliegue en Producción

### Configuraciones adicionales para producción:

1. **Variables de entorno**:
```bash
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

2. **Base de datos**:
```python
# Cambiar a PostgreSQL o MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'libreria_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Servidor web**:
```nginx
# Configuración Nginx con HTTPS
server {
    listen 443 ssl;
    server_name tu-dominio.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Métricas y Monitoreo

### Logs de Seguridad
Los eventos de seguridad se registran en `security.log`:
```
INFO - User login successful: usuario from IP 192.168.1.100
WARNING - Rate limit exceeded for IP 192.168.1.200 on auth endpoint
WARNING - Suspicious User-Agent detected from IP 192.168.1.300
ERROR - Permission denied for user usuario trying to access admin_dashboard
```

### Endpoints de Monitoreo
- `/api/admin/dashboard/` - Estadísticas del sistema
- Logs en tiempo real para administradores
- Métricas de uso de API por endpoint

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit changes (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Para reportar bugs o solicitar funcionalidades:
1. Crear un issue en GitHub
2. Incluir logs de error si aplica
3. Describir pasos para reproducir el problema

---

**Desarrollado con ❤️ para demostrar las mejores prácticas de seguridad en Django**