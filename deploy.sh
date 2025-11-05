#!/bin/bash

# Maharashtra AI Governance Platform Deployment Script

echo "🏛️ Deploying Maharashtra AI Governance Platform..."

# Set environment variables
export GOOGLE_CLOUD_PROJECT="maharashtra-governance"
export GOOGLE_APPLICATION_CREDENTIALS="service-account-key.json"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Authenticate with Google Cloud
echo "🔐 Authenticating with Google Cloud..."
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Enable required APIs
echo "🔧 Enabling Google Cloud APIs..."
gcloud services enable bigquery.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable iam.googleapis.com

# Create BigQuery datasets
echo "📊 Creating BigQuery datasets..."
bq mk --dataset --location=asia-south1 $GOOGLE_CLOUD_PROJECT:governance_data
bq mk --dataset --location=asia-south1 $GOOGLE_CLOUD_PROJECT:citizen_services
bq mk --dataset --location=asia-south1 $GOOGLE_CLOUD_PROJECT:predictions

# Deploy Cloud Functions (if needed)
echo "☁️ Deploying serverless functions..."
# gcloud functions deploy governance-api --runtime python39 --trigger-http

# Initialize platform
echo "🚀 Initializing platform..."
python main.py

echo "✅ Deployment complete!"
echo "🌐 Access dashboard at: http://localhost:8501"