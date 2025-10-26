<#
Simple PowerShell helper to create Secret Manager secrets for Cloud Run deployments.
Edit the variables below before running.
#>

param(
    [string]$ProjectId = "YOUR_PROJECT_ID",
    [string]$SecretKeyValue = "PUT_YOUR_SECRET_KEY_HERE",
    [string]$DatabaseUrlValue = "postgres://USER:PASSWORD@/DBNAME?host=/cloudsql/PROJECT:REGION:INSTANCE",
    [string]$GcsJsonPath = "" # Optional: path to service account JSON for GCS
)

if ($ProjectId -eq "YOUR_PROJECT_ID") {
    Write-Host "Please edit the script parameters before running (ProjectId, SecretKeyValue, DatabaseUrlValue)." -ForegroundColor Yellow
    exit 1
}

Write-Host "Setting gcloud project to $ProjectId"
gcloud config set project $ProjectId

Write-Host "Creating secret: django-secret-key"
gcloud secrets create django-secret-key --replication-policy="automatic" --project=$ProjectId
$SecretKeyValue | gcloud secrets versions add django-secret-key --data-file=- --project=$ProjectId

Write-Host "Creating secret: django-database-url"
gcloud secrets create django-database-url --replication-policy="automatic" --project=$ProjectId
$DatabaseUrlValue | gcloud secrets versions add django-database-url --data-file=- --project=$ProjectId

if ($GcsJsonPath -ne "") {
    Write-Host "Creating secret: gcs-service-account-json"
    gcloud secrets create gcs-service-account-json --replication-policy="automatic" --project=$ProjectId
    gcloud secrets versions add gcs-service-account-json --data-file=$GcsJsonPath --project=$ProjectId
}

Write-Host "Done. Remember to grant Secret Manager access to your Cloud Run service account." -ForegroundColor Green

Write-Host "Example IAM binding:"
Write-Host "gcloud projects add-iam-policy-binding $ProjectId --member='serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com' --role='roles/secretmanager.secretAccessor'"

Write-Host "Script complete." -ForegroundColor Cyan
