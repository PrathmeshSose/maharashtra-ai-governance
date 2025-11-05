from google.cloud import bigquery
from google.cloud import storage
import pandas as pd
from config import Config

class DataPipeline:
    def __init__(self):
        self.bq_client = bigquery.Client(project=Config.PROJECT_ID)
        self.storage_client = storage.Client()
        
    def create_datasets(self):
        """Create BigQuery datasets for governance data"""
        datasets = [
            f"{Config.PROJECT_ID}.{Config.DATASET_ID}",
            f"{Config.PROJECT_ID}.citizen_services",
            f"{Config.PROJECT_ID}.predictions"
        ]
        
        for dataset_id in datasets:
            try:
                self.bq_client.create_dataset(dataset_id)
                print(f"Created dataset: {dataset_id}")
            except Exception as e:
                print(f"Dataset exists or error: {e}")
    
    def load_sample_data(self):
        """Load sample governance data"""
        # Health data
        health_schema = [
            bigquery.SchemaField("district", "STRING"),
            bigquery.SchemaField("service_type", "STRING"),
            bigquery.SchemaField("request_count", "INTEGER"),
            bigquery.SchemaField("resolution_time", "FLOAT"),
            bigquery.SchemaField("date", "DATE"),
            bigquery.SchemaField("priority_score", "FLOAT")
        ]
        
        # Infrastructure data  
        infra_schema = [
            bigquery.SchemaField("district", "STRING"),
            bigquery.SchemaField("infrastructure_type", "STRING"),
            bigquery.SchemaField("maintenance_requests", "INTEGER"),
            bigquery.SchemaField("budget_allocated", "FLOAT"),
            bigquery.SchemaField("completion_rate", "FLOAT"),
            bigquery.SchemaField("date", "DATE")
        ]
        
        self._create_table("health_services", health_schema)
        self._create_table("infrastructure_services", infra_schema)
        
    def _create_table(self, table_name, schema):
        table_id = f"{Config.PROJECT_ID}.{Config.DATASET_ID}.{table_name}"
        table = bigquery.Table(table_id, schema=schema)
        try:
            self.bq_client.create_table(table)
            print(f"Created table: {table_name}")
        except Exception as e:
            print(f"Table exists or error: {e}")
    
    def get_training_data(self):
        """Fetch data for ML training"""
        query = f"""
        SELECT 
            district,
            service_type,
            request_count,
            resolution_time,
            priority_score,
            EXTRACT(MONTH FROM date) as month,
            EXTRACT(DAYOFWEEK FROM date) as day_of_week
        FROM `{Config.PROJECT_ID}.{Config.DATASET_ID}.health_services`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 YEAR)
        """
        return self.bq_client.query(query).to_dataframe()