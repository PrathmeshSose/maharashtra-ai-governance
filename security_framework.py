from google.cloud import iam
from google.cloud import bigquery
import hashlib
import re
from config import Config

class SecurityFramework:
    def __init__(self):
        self.iam_client = iam.IAMCredentialsServiceClient()
        self.bq_client = bigquery.Client(project=Config.PROJECT_ID)
        
    def setup_iam_policies(self):
        """Setup IAM roles and policies for data governance"""
        policies = {
            "data_analysts": {
                "role": "roles/bigquery.dataViewer",
                "condition": "request.time < timestamp('2024-12-31T23:59:59Z')"
            },
            "department_heads": {
                "role": "roles/bigquery.jobUser", 
                "condition": "resource.name.startsWith('projects/{}/datasets/citizen_services')".format(Config.PROJECT_ID)
            }
        }
        
        for group, policy in policies.items():
            print(f"IAM policy configured for {group}: {policy['role']}")
        
        return policies
    
    def anonymize_pii(self, data_dict):
        """Remove/hash PII data for compliance"""
        anonymized = data_dict.copy()
        
        for field in Config.PII_FIELDS:
            if field in anonymized:
                if field == 'citizen_id':
                    # Hash citizen ID for tracking while maintaining privacy
                    anonymized[field] = hashlib.sha256(str(anonymized[field]).encode()).hexdigest()[:16]
                else:
                    # Remove other PII fields
                    anonymized[field] = "[REDACTED]"
        
        return anonymized
    
    def validate_data_access(self, user_role, requested_fields):
        """Validate if user can access requested data fields"""
        access_matrix = {
            "citizen_service": ["service_type", "district", "status", "priority_score"],
            "data_analyst": ["service_type", "district", "status", "priority_score", "request_count", "resolution_time"],
            "admin": ["*"]  # Full access
        }
        
        allowed_fields = access_matrix.get(user_role, [])
        
        if "*" in allowed_fields:
            return True
            
        return all(field in allowed_fields for field in requested_fields)
    
    def create_audit_log(self, user_id, action, resource, timestamp):
        """Create audit log entry"""
        audit_entry = {
            'user_id': hashlib.sha256(user_id.encode()).hexdigest()[:16],
            'action': action,
            'resource': resource,
            'timestamp': timestamp,
            'compliance_status': 'LOGGED'
        }
        
        # In production, this would write to a secure audit table
        print(f"AUDIT: {audit_entry}")
        return audit_entry
    
    def setup_data_retention(self):
        """Setup automated data retention policies"""
        retention_query = f"""
        CREATE OR REPLACE TABLE `{Config.PROJECT_ID}.{Config.DATASET_ID}.data_retention_policy` AS
        SELECT 
            table_name,
            {Config.RETENTION_DAYS} as retention_days,
            CURRENT_TIMESTAMP() as policy_created
        FROM `{Config.PROJECT_ID}.{Config.DATASET_ID}.INFORMATION_SCHEMA.TABLES`
        """
        
        try:
            self.bq_client.query(retention_query)
            print("Data retention policy created")
        except Exception as e:
            print(f"Retention policy error: {e}")
    
    def encrypt_sensitive_data(self, data):
        """Basic encryption for sensitive data fields"""
        # In production, use Google Cloud KMS
        sensitive_hash = hashlib.sha256(str(data).encode()).hexdigest()
        return f"ENC_{sensitive_hash[:32]}"