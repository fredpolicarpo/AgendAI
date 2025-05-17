# Cloud Functions for AgendAI

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "dialogflow.googleapis.com",
    "aiplatform.googleapis.com",
    "calendar-json.googleapis.com",
    "sheets.googleapis.com"
  ])
  
  project = var.gcp_project_id
  service = each.key
  
  disable_dependent_services = false
  disable_on_destroy         = false
}

# Cloud Storage bucket for function source code
resource "google_storage_bucket" "function_bucket" {
  name     = "${var.gcp_project_id}-functions"
  location = var.gcp_region
  
  uniform_bucket_level_access = true
  
  depends_on = [google_project_service.required_apis]
}

# Archive the function source code
data "archive_file" "function_zip" {
  type        = "zip"
  output_path = "${path.module}/function-source.zip"
  
  source_dir = "${path.module}/../src"
  
  excludes = [
    "__pycache__",
    "*.pyc",
    "*.pyo"
  ]
}

# Upload the function source code to the bucket
resource "google_storage_bucket_object" "function_source" {
  name   = "function-source-${data.archive_file.function_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_zip.output_path
}

# Cloud Function for Dialogflow CX webhook
resource "google_cloudfunctions2_function" "dialogflow_webhook" {
  name     = "agendai-dialogflow-webhook"
  location = var.gcp_region
  
  build_config {
    runtime     = "python310"
    entry_point = "handle_dialogflow_webhook"
    
    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.function_source.name
      }
    }
  }
  
  service_config {
    max_instance_count = 10
    min_instance_count = 0
    available_memory   = "256Mi"
    timeout_seconds    = 60
    
    environment_variables = {
      GOOGLE_CLOUD_PROJECT = var.gcp_project_id
      PROFESSIONAL_CONFIG_SHEET_ID = var.professional_config_sheet_id
      BOOKING_LOG_SHEET_ID = var.booking_log_sheet_id
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = var.gcp_project_id
  location       = var.gcp_region
  cloud_function = google_cloudfunctions2_function.dialogflow_webhook.name
  
  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

# Dialogflow CX Agent
resource "google_dialogflow_cx_agent" "agendai_agent" {
  display_name          = var.dialogflow_cx_agent_display_name
  location              = var.gcp_region
  default_language_code = "pt-br"
  time_zone             = "America/Sao_Paulo"
  
  depends_on = [google_project_service.required_apis]
}

# Output the Cloud Function URL
output "webhook_url" {
  value       = google_cloudfunctions2_function.dialogflow_webhook.service_config[0].uri
  description = "The URL of the deployed Cloud Function"
}

# Output the Dialogflow CX Agent ID
output "dialogflow_cx_agent_id" {
  value       = google_dialogflow_cx_agent.agendai_agent.id
  description = "The ID of the created Dialogflow CX Agent"
}
