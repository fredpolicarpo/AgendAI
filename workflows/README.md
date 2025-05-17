# AgendAI n8n Workflows

This directory contains n8n workflows for the AgendAI scheduling assistant.

## Overview

These workflows implement the appointment scheduling functionality described in the product specification, integrating with:

- Google Calendar for appointment scheduling and availability management
- Google Sheets for logging and reporting
- Chatbot platform for user interactions

## Available Workflows

- `appointment_scheduling.json` - Main workflow for appointment scheduling logic
- `reminders.json` - Workflow for sending appointment reminders
- `reporting.json` - Workflow for generating professional reports

## Setup Instructions

1. Import these workflows into your n8n instance
2. Configure the Google Calendar and Google Sheets credentials
3. Set up webhooks for integration with your chatbot platform
4. Customize workflow parameters according to your specific requirements

## Required n8n Nodes

- Google Calendar
- Google Sheets
- Webhook
- HTTP Request
- Function
- IF/Switch
- Set
- SplitInBatches
