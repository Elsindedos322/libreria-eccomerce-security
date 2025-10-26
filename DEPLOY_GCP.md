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

## Secret Manager (opcional pero recomendado)

Guardar secretos sensibles (SECRET_KEY, DATABASE_URL, credenciales de GCS si las necesitas) en Secret Manager es una práctica recomendable. A continuación tienes comandos y un pequeño flujo para crear secretos y dar acceso a Cloud Run.

1) Crear secretos en Secret Manager

En PowerShell (reemplaza valores por los tuyos):

```powershell
# Crear secretos
gcloud secrets create django-secret-key --replication-policy="automatic"
echo -n "YOUR_LONG_SECRET_KEY" | gcloud secrets versions add django-secret-key --data-file=-

gcloud secrets create django-database-url --replication-policy="automatic"
echo -n "postgres://USER:PASSWORD@/DBNAME?host=/cloudsql/PROJECT:REGION:INSTANCE" | gcloud secrets versions add django-database-url --data-file=-

# (Opcional) credenciales JSON para GCS
gcloud secrets create gcs-service-account-json --replication-policy="automatic"
gcloud secrets versions add gcs-service-account-json --data-file="path\to\service-account.json"
```

2) Dar permiso a la cuenta de servicio de Cloud Run para acceder a los secretos

Identifica la cuenta de servicio que usará Cloud Run (por ejemplo: `PROJECT_NUMBER-compute@developer.gserviceaccount.com` o una creada por ti). Luego otorga el rol `roles/secretmanager.secretAccessor`:

```powershell
gcloud projects get-iam-policy PROJECT_ID --format=json

# Ejemplo para dar acceso
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

3) Usar secretos desde Cloud Run

Al desplegar con `gcloud run deploy` puedes mapear secrets a variables de entorno usando `--set-secrets`:

```powershell
gcloud run deploy mi-django-app `
  --image REGION-docker.pkg.dev/PROJECT/REPO/django-app:v1 `
  --platform managed `
  --region REGION `
  --allow-unauthenticated `
  --set-secrets SECRET_KEY=django-secret-key:latest,DATABASE_URL=django-database-url:latest `
  --update-env-vars DJANGO_SETTINGS_MODULE=libreria.libreria.settings,GS_BUCKET_NAME=mi-proyecto-django-assets
```

Esto inyectará las versiones más recientes de `django-secret-key` y `django-database-url` como variables de entorno dentro del contenedor.

4) Nota sobre GCS credentials

Si usas la cuenta de servicio que Cloud Run ya proporciona (o una cuenta dedicada) y le das permisos de Storage Object Admin sobre el bucket, normalmente no necesitas subir el JSON a Secret Manager. En cambio, si necesitas que el contenedor use un service-account JSON (por ejemplo para local testing), puedes almacenar ese JSON en Secret Manager y cargarlo en el contenedor como variable o fichero temporal al inicio.

5) Pequeño helper PowerShell para crear los secretos (repo)

He incluido un script de ejemplo `scripts\gcp_create_secrets.ps1` que automatiza la creación de los tres secretos (SECRET_KEY, DATABASE_URL, opcional GCS JSON). Revisa y ajusta antes de ejecutarlo.

---

Si quieres, puedo añadir el script `scripts\gcp_create_secrets.ps1` ahora y también un ejemplo de `cloudbuild.yaml` que use Secret Manager en Cloud Build para despliegues automáticos. ¿Lo agrego ahora?

