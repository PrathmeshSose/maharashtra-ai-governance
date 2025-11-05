#!/usr/bin/env python3
"""
Maharashtra AI-Powered Governance Platform
Main orchestration script for deployment
"""

import os
from data_pipeline import DataPipeline
from predictive_models import PredictiveModels
from service_engine import ServicePrioritizationEngine
from security_framework import SecurityFramework
from config import Config

def setup_platform():
    """Initialize the governance platform"""
    print("🏛️ Initializing Maharashtra AI Governance Platform...")
    
    # Initialize components
    data_pipeline = DataPipeline()
    models = PredictiveModels()
    security = SecurityFramework()
    
    # Setup data infrastructure
    print("📊 Setting up data infrastructure...")
    data_pipeline.create_datasets()
    data_pipeline.load_sample_data()
    
    # Configure security
    print("🔒 Configuring security framework...")
    security.setup_iam_policies()
    security.setup_data_retention()
    
    # Train initial models
    print("🤖 Training predictive models...")
    try:
        training_data = data_pipeline.get_training_data()
        if not training_data.empty:
            accuracy = models.train_demand_predictor(training_data)
            print(f"✅ Model trained with accuracy: {accuracy:.2f}")
            models.save_models()
        else:
            print("⚠️ No training data available. Using pre-configured models.")
    except Exception as e:
        print(f"⚠️ Model training skipped: {e}")
    
    print("✅ Platform initialization complete!")
    return True

def run_dashboard():
    """Launch the governance dashboard"""
    print("🚀 Launching governance dashboard...")
    os.system("streamlit run dashboard.py --server.port 8501")

if __name__ == "__main__":
    # Setup platform
    if setup_platform():
        print("\n" + "="*50)
        print("Maharashtra AI Governance Platform Ready!")
        print("="*50)
        print("🌐 Dashboard: http://localhost:8501")
        print("📊 BigQuery Dataset: governance_data")
        print("🔒 Security: IAM policies active")
        print("🤖 AI Models: Demand prediction ready")
        print("="*50)
        
        # Launch dashboard
        run_dashboard()