# 🔐 Librería E‑commerce centrada en Seguridad (Django 5)

> E‑commerce de libros con autenticación JWT y Google, control de roles/permisos, rate limiting, validación de entradas y headers de seguridad. Incluye catálogo con carrusel y carrito protegido por permisos.

## ⚙️ Instalación y ejecución rápida (Windows PowerShell)

Prerrequisitos: Python 3.12+, Git.

```powershell
# 1) Crear y activar entorno virtual
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Migraciones (carpeta proyecto)
cd .\libreria; python manage.py migrate

# 4) Datos de ejemplo (opcional)
python manage.py create_sample_books

# 5) Ejecutar
python manage.py runserver 127.0.0.1:8000
```

Variables `.env` (crear archivo en `libreria/.env`):
```
SECRET_KEY=changeme-dev
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# Para pruebas locales con DEBUG=False (evita redirigir a HTTPS)
SECURE_SSL_REDIRECT=False

# OAuth Google (opcional)
GOOGLE_OAUTH2_CLIENT_ID=
GOOGLE_OAUTH2_CLIENT_SECRET=
```

Estáticos con DEBUG=False (solo local):
- Ejecuta `python manage.py collectstatic` tras cambios en `theme/static/`.
- La app mapea `/static/` a `STATIC_ROOT` en modo no‑debug para uso con runserver local.

## 🔐 Seguridad implementada (resumen)
- JWT (access/refresh), expiración y refresco seguro.
- OAuth2 Google vía django‑allauth.
- Sistema de roles y permisos (ADMIN, MODERATOR, USER, GUEST) aplicado en vistas web y API.
- Rate‑limiting por IP/endpoint.
- Validación y sanitización de parámetros (anti‑XSS/SQLi/path traversal).
- CORS controlado para dev/producción.
- Logging de seguridad (security.log) con eventos clave.
- Cabeceras de seguridad (HSTS, X‑Frame‑Options, X‑Content‑Type‑Options, X‑XSS‑Protection, CSP sugerida).

## 🌐 Endpoints principales

Auth/JWT
```
POST /api/auth/register/
POST /api/auth/login/
GET  /api/auth/profile/
POST /api/token/
POST /api/token/refresh/
```
Libros
```
GET  /api/books/
GET  /api/books/{id}/
POST /api/books/create/   (Admin/Mod)
PUT  /api/books/{id}/update/ (Admin/Mod)
DEL  /api/books/{id}/delete/  (Admin/Mod)
```
Carrito
```
GET  /api/cart/
POST /api/cart/add/
DEL  /api/cart/remove/{id}/
```
Administración
```
GET /api/admin/dashboard/
GET /api/admin/users/
```

## 🧪 Probar seguridad rápidamente
```powershell
# Perfil con sesión (navegador): /accounts/login/
# API: usa /api/token/ y envía Authorization: Bearer <ACCESS>
python .\test_api_security.py
```

## 🔒 Detalles de seguridad
- Rate limits ejemplo: auth 5 req/5m, admin 10 req/5m, API 100 req/h.
- Validaciones: regex seguro en búsquedas, límites de longitud, tipos estrictos.
- Headers de seguridad típicos:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; img-src 'self' data: https:; script-src 'self' 'unsafe-inline' https:; style-src 'self' 'unsafe-inline' https:
```

## 🚀 Producción (resumen)
1) Variables
```
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
ALLOWED_HOSTS=tu-dominio.com
```
2) DB recomendada: PostgreSQL.
3) Servir estáticos
```nginx
location /static/ { alias /var/www/libreria/static/; }
location /media/  { alias /var/www/libreria/media/; }
```
4) Alternativa simple: WhiteNoise (middleware) para estáticos sin Nginx.

---

Hecho con foco en “defensa en profundidad” para proyectos Django.