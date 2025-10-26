Preparación y despliegue a Google Cloud (Cloud Run + Cloud SQL)

Resumen rápido:
- Usar PostgreSQL en Cloud SQL.
- Conectar Cloud Run a Cloud SQL mediante la Conexión de instancia (Unix socket).
- Proveer `DATABASE_URL` en el formato esperado por dj-database-url.

Pasos mínimos locales:

1) Instalar dependencias de producción

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
``` 

2) Preparar variables de entorno (local / migración via cloud-sql-proxy)

Para migrar localmente usando el proxy de Cloud SQL, exporta una DATABASE_URL apuntando al proxy (en PowerShell):

```powershell
$env:DATABASE_URL = "postgres://postgres:TU_PASS@127.0.0.1:5432/django_prod_db"
$env:SECRET_KEY = "cualquier_clave_segura_para_local"
$env:DEBUG = "False"
```

3) Usar cloud_sql_proxy para conectar localmente (opcional, para migraciones)

- Instala y ejecuta el proxy, por ejemplo:

```powershell
# Descarga cloud_sql_proxy y ejecútalo, o usa gcloud components
cloud_sql_proxy.exe YOUR_PROJECT:REGION:INSTANCE --port=5432
```

4) Migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

5) Construir imagen y desplegar (Cloud Run)

- Build y push (usando Artifact Registry or Container Registry):

```powershell
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT/REPO/django-app:v1
```

- Deploy en Cloud Run. Importante: configura la Conexión a Cloud SQL desde la página de Cloud Run (añade la instancia) y utiliza DATABASE_URL con host `/cloudsql/INSTANCE_CONNECTION_NAME`:

```powershell
$cloudsql = "PROJECT:REGION:INSTANCE"
$env:SECRET_KEY = "<PRODUCTION_SECRET>"
$env:DATABASE_URL = "postgres://USER:PASSWORD@/DBNAME?host=/cloudsql/$cloudsql"

gcloud run deploy mi-django-app `
  --image REGION-docker.pkg.dev/PROJECT/REPO/django-app:v1 `
  --platform managed `
  --region REGION `
  --allow-unauthenticated `
  --update-env-vars DJANGO_SETTINGS_MODULE=libreria.libreria.settings,SECRET_KEY=$env:SECRET_KEY,DATABASE_URL=$env:DATABASE_URL
```

Notas y recomendaciones:
- No pongas claves en el repo. Usa Secret Manager o variables de entorno del servicio.
- Para archivos estáticos: usar Cloud Storage + WhiteNoise or Cloud Storage backed storage.
- Añade `gunicorn` y `psycopg2-binary` (ya añadidos a requirements.txt).
- Comprueba `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE` y HSTS sólo en producción.

