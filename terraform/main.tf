    // main.tf
    // Configuração do provider Google Cloud e definições do projeto.

    terraform {
      required_providers {
        google = {
          source  = "hashicorp/google"
          version = "~> 5.0"
        }
      }
      required_version = ">= 1.0"
    }

    provider "google" {
      project = var.gcp_project_id
      region  = var.gcp_region
      zone    = var.gcp_zone
    }

    resource "google_project_service" "project_services" {
      project                    = var.gcp_project_id
      for_each                   = toset(var.gcp_project_apis)
      service                    = each.key
      disable_dependent_services = true // Desativa serviços dependentes se o serviço principal for desativado
      disable_on_destroy         = false // Mantém as APIs ativas mesmo se o recurso Terraform for destruído (recomendado para APIs)
    }

    // Opcional: Criação da conta de serviço para as Cloud Functions, se não quiser usar a default.
    // Para P1, a conta de serviço default da Cloud Function pode ser suficiente com os papéis corretos.
    resource "google_service_account" "cloud_function_sa" {
      project      = var.gcp_project_id
      account_id   = "${var.service_prefix}-cf-sa"
      display_name = "AgendAI Cloud Functions Service Account"
      description  = "Conta de serviço para as Cloud Functions do AgendAI"
    }

    output "cloud_function_service_account_email" {
      description = "O email da conta de serviço das Cloud Functions."
      value       = google_service_account.cloud_function_sa.email
    }
    