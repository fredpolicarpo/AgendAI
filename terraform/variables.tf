variable "gcp_project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "gcp_region" {
  description = "The Google Cloud region to deploy resources"
  type        = string
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "The Google Cloud zone within the region"
  type        = string
  default     = "us-central1-a"
}

variable "gcp_project_apis" {
  description = "List of Google Cloud APIs to enable for the project"
  type        = list(string)
  default = [
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "dialogflow.googleapis.com",
    "aiplatform.googleapis.com",
    "calendar-json.googleapis.com",
    "sheets.googleapis.com"
  ]
}

variable "service_prefix" {
  description = "Prefix to use for service names"
  type        = string
  default     = "agendai"
}

# Add other variables needed for the AgendAI project
variable "dialogflow_cx_agent_display_name" {
  description = "The display name for the Dialogflow CX agent"
  type        = string
  default     = "AgendAI Assistant"
}

variable "professional_config_sheet_id" {
  description = "The ID of the Google Sheet for professional configuration"
  type        = string
  default     = ""
}

variable "booking_log_sheet_id" {
  description = "The ID of the Google Sheet for booking logs"
  type        = string
  default     = ""
}
