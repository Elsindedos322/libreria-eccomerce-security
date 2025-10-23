# Seguridad y autenticaciones: guía de demo (Windows PowerShell)

Esta guía muestra cómo evidenciar las capas de seguridad implementadas: JWT, roles/permiso, validaciones, rate limiting, CORS y logging.

Requisitos previos:
- Servidor en marcha desde la carpeta `libreria` con la venv:
  ```powershell
  cd "E:\Carreras tecnicas etc\Tecsup\Tecsup ciclo 5\Desarrollo de Soluciones en la Nube\libreria-ecommerce-feature-google-login\libreria"
  & "..\.venv\Scripts\python.exe" manage.py runserver
  ```
- (Opcional) Datos de ejemplo y usuarios de prueba:
  ```powershell
  & "..\.venv\Scripts\python.exe" manage.py create_sample_books
  & "..\.venv\Scripts\python.exe" manage.py create_test_users
  ```

## 1) Registro y login con JWT

- Registro (devuelve usuario seguro + tokens):
  ```powershell
  $body = @{ username = "demo"; email = "demo@example.com"; password = "Demo123!"; password_confirm = "Demo123!"; first_name = "Demo"; last_name = "User" } | ConvertTo-Json
  Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/auth/register/ -ContentType 'application/json' -Body $body
  ```
- Login con email y password:
  ```powershell
  $login = @{ email = "demo@example.com"; password = "Demo123!" } | ConvertTo-Json
  $resp = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/auth/login/ -ContentType 'application/json' -Body $login
  $token = $resp.tokens.access
  $refresh = $resp.tokens.refresh
  $token
  ```
- Usar el token para obtener perfil:
  ```powershell
  Invoke-RestMethod -Headers @{ Authorization = "Bearer $token" } -Uri http://127.0.0.1:8000/api/auth/profile/
  ```

Captura sugerida: pantalla de /accounts/login/ (allauth) y la respuesta JSON de login con `access`/`refresh` (oculta el token si lo publicarás).

## 2) Acceso denegado por rol

Endpoint administrativo protegido: `/api/admin/dashboard/`

- Como usuario normal, debe responder 403:
  ```powershell
  Invoke-RestMethod -Headers @{ Authorization = "Bearer $token" } -Uri http://127.0.0.1:8000/api/admin/dashboard/ -ErrorAction SilentlyContinue | ConvertTo-Json
  $LASTEXITCODE
  ```

- Promocionar a ADMIN y reintentar:
  ```powershell
  & "..\.venv\Scripts\python.exe" manage.py set_user_role --username demo --role ADMIN
  # genera un nuevo token si lo necesitas
  $resp = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/auth/login/ -ContentType 'application/json' -Body $login
  $token = $resp.tokens.access
  Invoke-RestMethod -Headers @{ Authorization = "Bearer $token" } -Uri http://127.0.0.1:8000/api/admin/dashboard/
  ```

## 3) Validaciones y campos filtrados

- Listado de libros público con filtro seguro:
  ```powershell
  Invoke-RestMethod http://127.0.0.1:8000/api/books/?search=python | ConvertTo-Json -Depth 5
  ```
- Intento de inyección (se rechaza y se loggea):
  ```powershell
  Invoke-WebRequest http://127.0.0.1:8000/api/books/?search=python;DROP%20TABLE -UseBasicParsing
  Get-Content ..\security.log -Tail 20
  ```
- Endpoint con filtrado por rol: `/api/admin/users/`
  - Usuario normal: verás campos básicos (id, username, nombres)
  - ADMIN: verás email y date_joined agregados
  ```powershell
  # como admin
  Invoke-RestMethod -Headers @{ Authorization = "Bearer $token" } -Uri http://127.0.0.1:8000/api/admin/users/ | ConvertTo-Json -Depth 5
  ```

## 4) Rate limiting y CORS

- Rate limiting en auth (5 peticiones/5 min por IP):
  ```powershell
  1..6 | ForEach-Object {
    try { Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/auth/login/ -ContentType 'application/json' -Body $login }
    catch { $_.Exception.Response | Format-List * }
  }
  ```
  La sexta debe devolver 429.

- CORS/headers de seguridad (revisa encabezados):
  ```powershell
  (Invoke-WebRequest http://127.0.0.1:8000/api/books/ -UseBasicParsing).Headers
  ```

## 5) OAuth2 con Google (opcional)

- Define en `.env`:
  - `GOOGLE_OAUTH2_CLIENT_ID` y `GOOGLE_OAUTH2_CLIENT_SECRET`
- En admin crea un SocialApp de Google y asócialo al Site 1. Callback típico: `http://127.0.0.1:8000/accounts/google/login/callback/`
- Flujo: `/accounts/login/` → "Sign in with Google".

## 6) HTTPS en despliegue

- Ajustes ya listos en `settings.py` (HSTS, cookies seguras, redirect) cuando `DEBUG=False`.
- Opción rápida: reversa con Nginx/Traefik y Let’s Encrypt, o proxy Cloudflare. Verifica que el navegador muestre el candado.

---
Logs en `security.log` (raíz del proyecto). Usa `Get-Content ..\security.log -Tail 100 -Wait` para verlos en vivo.
