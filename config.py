import os
from dataclasses import dataclass

@dataclass
class Config:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "maharashtra-governance")
    REGION = "asia-south1"
    DATASET_ID = "governance_data"
    MODEL_ENDPOINT = "projects/{}/locations/{}/endpoints/{}".format(PROJECT_ID, REGION, "governance-predictor")
    
    # Security & Compliance
    IAM_ROLES = {
        "data_analyst": "roles/bigquery.dataViewer",
        "admin": "roles/bigquery.admin",
        "citizen_service": "roles/aiplatform.user"
    }
    
    # Data Privacy Settings
    PII_FIELDS = ["citizen_id", "phone", "address", "aadhaar"]
    RETENTION_DAYS = 2555  # 7 years as per Indian data laws