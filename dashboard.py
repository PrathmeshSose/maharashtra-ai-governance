import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from data_pipeline import DataPipeline
from predictive_models import PredictiveModels
from service_engine import ServicePrioritizationEngine
from security_framework import SecurityFramework

class GovernanceDashboard:
    def __init__(self):
        self.data_pipeline = DataPipeline()
        self.models = PredictiveModels()
        self.security = SecurityFramework()
        
    def run(self):
        st.set_page_config(page_title="Maharashtra AI Governance", layout="wide")
        
        st.title("🏛️ Maharashtra AI-Powered Governance Platform")
        st.sidebar.title("Navigation")
        
        # User authentication simulation
        user_role = st.sidebar.selectbox("User Role", ["citizen_service", "data_analyst", "admin"])
        
        # Main navigation
        page = st.sidebar.radio("Select Dashboard", [
            "Executive Overview",
            "Predictive Analytics", 
            "Service Prioritization",
            "Citizen Insights",
            "Compliance Monitor"
        ])
        
        if page == "Executive Overview":
            self.executive_overview()
        elif page == "Predictive Analytics":
            self.predictive_analytics()
        elif page == "Service Prioritization":
            self.service_prioritization()
        elif page == "Citizen Insights":
            self.citizen_insights()
        elif page == "Compliance Monitor":
            self.compliance_monitor()
    
    def executive_overview(self):
        st.header("📊 Executive Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Requests", "2,847", "+12%")
        with col2:
            st.metric("Avg Resolution Time", "4.2 days", "-0.8 days")
        with col3:
            st.metric("Citizen Satisfaction", "4.1/5", "+0.3")
        with col4:
            st.metric("Budget Efficiency", "87%", "+5%")
        
        # Sample data for visualization
        districts = ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad']
        service_counts = [450, 380, 290, 220, 180]
        
        fig = px.bar(x=districts, y=service_counts, title="Service Requests by District")
        st.plotly_chart(fig, use_container_width=True)
        
        # Priority heatmap
        priority_data = pd.DataFrame({
            'District': districts * 3,
            'Service Type': ['Health'] * 5 + ['Infrastructure'] * 5 + ['Safety'] * 5,
            'Priority Score': [85, 72, 68, 55, 48, 78, 65, 58, 45, 42, 92, 88, 75, 62, 58]
        })
        
        fig_heatmap = px.density_heatmap(
            priority_data, x='District', y='Service Type', z='Priority Score',
            title="Service Priority Heatmap"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    def predictive_analytics(self):
        st.header("🔮 Predictive Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            district = st.selectbox("Select District", ['Mumbai', 'Pune', 'Nagpur'])
            service_type = st.selectbox("Service Type", ['Health', 'Infrastructure', 'Safety'])
            
        with col2:
            month = st.slider("Month", 1, 12, datetime.now().month)
            day_of_week = st.slider("Day of Week", 1, 7, datetime.now().weekday() + 1)
        
        if st.button("Generate Prediction"):
            # Simulate prediction
            predicted_demand = self.models.predict_service_demand(
                district, service_type, month, day_of_week, 4.5
            ) or 125
            
            st.success(f"Predicted demand for {service_type} in {district}: **{predicted_demand} requests**")
            
            # Forecast chart
            dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
            forecast = [predicted_demand + (i * 2) + (i % 7 * 10) for i in range(30)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=forecast, mode='lines+markers', name='Predicted Demand'))
            fig.update_layout(title="30-Day Service Demand Forecast")
            st.plotly_chart(fig, use_container_width=True)
    
    def service_prioritization(self):
        st.header("⚡ Service Prioritization Engine")
        
        st.subheader("Submit New Service Request")
        
        with st.form("service_request"):
            citizen_query = st.text_area("Describe the service request")
            district = st.selectbox("District", ['Mumbai', 'Pune', 'Nagpur', 'Nashik'])
            feedback_score = st.slider("Citizen Feedback Score", 1, 5, 3)
            
            if st.form_submit_button("Process Request"):
                if citizen_query:
                    # Simulate service routing
                    request_data = {
                        'id': f"REQ_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        'description': citizen_query,
                        'district': district,
                        'citizen_feedback_score': feedback_score
                    }
                    
                    # Mock routing result
                    routing_result = {
                        'request_id': request_data['id'],
                        'assigned_department': 'Health Services',
                        'priority_score': 75,
                        'estimated_resolution': 5,
                        'service_category': 'health'
                    }
                    
                    st.success("Request processed successfully!")
                    st.json(routing_result)
        
        # Active requests table
        st.subheader("Active High-Priority Requests")
        sample_requests = pd.DataFrame({
            'Request ID': ['REQ_001', 'REQ_002', 'REQ_003'],
            'District': ['Mumbai', 'Pune', 'Nagpur'],
            'Category': ['Health', 'Infrastructure', 'Safety'],
            'Priority Score': [92, 88, 85],
            'Status': ['In Progress', 'Assigned', 'Pending']
        })
        st.dataframe(sample_requests, use_container_width=True)
    
    def citizen_insights(self):
        st.header("👥 Citizen Insights")
        
        # Satisfaction trends
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        satisfaction = [3.8 + (i % 10) * 0.1 + (i % 3) * 0.05 for i in range(30)]
        
        fig = px.line(x=dates, y=satisfaction, title="Citizen Satisfaction Trend (30 Days)")
        fig.update_yaxis(range=[3.5, 4.5])
        st.plotly_chart(fig, use_container_width=True)
        
        # Service category breakdown
        categories = ['Health', 'Infrastructure', 'Safety', 'Education', 'Other']
        counts = [35, 28, 20, 12, 5]
        
        fig_pie = px.pie(values=counts, names=categories, title="Service Requests by Category")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    def compliance_monitor(self):
        st.header("🔒 Compliance & Security Monitor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Data Privacy Score", "98%", "+2%")
            st.metric("Audit Compliance", "100%", "0%")
            
        with col2:
            st.metric("Access Violations", "0", "0")
            st.metric("Data Retention", "Active", "✅")
        
        # Audit log sample
        st.subheader("Recent Audit Activities")
        audit_data = pd.DataFrame({
            'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(5)],
            'User': ['user_001', 'user_002', 'user_003', 'user_001', 'user_004'],
            'Action': ['DATA_ACCESS', 'QUERY_EXECUTE', 'REPORT_GENERATE', 'DATA_EXPORT', 'MODEL_TRAIN'],
            'Status': ['SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS']
        })
        st.dataframe(audit_data, use_container_width=True)

if __name__ == "__main__":
    dashboard = GovernanceDashboard()
    dashboard.run()