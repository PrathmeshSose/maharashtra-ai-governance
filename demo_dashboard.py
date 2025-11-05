import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import google.generativeai as genai
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GovernanceDashboard:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        
    def run(self):
        st.set_page_config(page_title="Maharashtra AI Governance", layout="wide")
        
        st.title("🏛️ Maharashtra AI-Powered Governance Platform")
        st.sidebar.title("Navigation")
        
        # User authentication simulation
        user_role = st.sidebar.selectbox("User Role", ["citizen_service", "data_analyst", "admin"])
        
        # Main navigation
        page = st.sidebar.radio("Select Dashboard", [
            "Executive Overview",
            "AI Service Engine", 
            "Predictive Analytics",
            "Citizen Insights"
        ])
        
        if page == "Executive Overview":
            self.executive_overview()
        elif page == "AI Service Engine":
            self.ai_service_engine()
        elif page == "Predictive Analytics":
            self.predictive_analytics()
        elif page == "Citizen Insights":
            self.citizen_insights()
    
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
            st.metric("AI Efficiency", "87%", "+5%")
        
        # District-wise service requests
        districts = ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad']
        service_counts = [450, 380, 290, 220, 180]
        
        fig = px.bar(x=districts, y=service_counts, 
                    title="Service Requests by District",
                    color=service_counts,
                    color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
        
        # Priority heatmap
        priority_data = pd.DataFrame({
            'District': districts * 3,
            'Service Type': ['Health'] * 5 + ['Infrastructure'] * 5 + ['Safety'] * 5,
            'Priority Score': [85, 72, 68, 55, 48, 78, 65, 58, 45, 42, 92, 88, 75, 62, 58]
        })
        
        fig_heatmap = px.density_heatmap(
            priority_data, x='District', y='Service Type', z='Priority Score',
            title="Service Priority Heatmap",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    def ai_service_engine(self):
        st.header("🤖 AI-Powered Service Engine")
        
        st.subheader("Citizen Query Analysis & Routing")
        
        with st.form("service_request"):
            citizen_query = st.text_area("Enter citizen service request:", 
                                       placeholder="e.g., Water supply issue in my area, need medical assistance...")
            district = st.selectbox("District", ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad'])
            
            if st.form_submit_button("🔍 Analyze with AI"):
                if citizen_query:
                    with st.spinner("AI analyzing request..."):
                        try:
                            # Use Gemini to analyze the query
                            prompt = f"""
                            Analyze this citizen service request for Maharashtra government:
                            
                            Query: {citizen_query}
                            District: {district}
                            
                            Provide analysis in this format:
                            - Service Category: [health/infrastructure/safety/education/other]
                            - Urgency Level: [low/medium/high/critical]
                            - Department: [specific department name]
                            - Estimated Resolution: [number] days
                            - Priority Score: [1-100]
                            - Action Required: [brief description]
                            """
                            
                            response = self.model.generate_content(prompt)
                            
                            st.success("✅ AI Analysis Complete!")
                            st.markdown("### 🎯 AI Analysis Results:")
                            st.markdown(response.text)
                            
                            # Generate routing decision
                            routing_prompt = f"""
                            Based on this analysis: {response.text}
                            
                            Generate a routing decision with:
                            1. Assigned Officer/Department
                            2. Timeline for resolution
                            3. Required resources
                            4. Citizen communication message
                            
                            Keep it concise and actionable.
                            """
                            
                            routing_response = self.model.generate_content(routing_prompt)
                            
                            st.markdown("### 📋 Routing Decision:")
                            st.info(routing_response.text)
                            
                        except Exception as e:
                            st.error(f"AI analysis failed: {str(e)}")
                            st.info("Please check your Gemini API key in the .env file")
        
        # Recent AI-processed requests
        st.subheader("📊 Recent AI-Processed Requests")
        sample_requests = pd.DataFrame({
            'Request ID': ['REQ_001', 'REQ_002', 'REQ_003', 'REQ_004'],
            'District': ['Mumbai', 'Pune', 'Nagpur', 'Mumbai'],
            'Category': ['Health', 'Infrastructure', 'Safety', 'Education'],
            'AI Priority Score': [92, 88, 85, 78],
            'Status': ['Routed', 'In Progress', 'Resolved', 'Pending'],
            'AI Confidence': ['95%', '89%', '92%', '87%']
        })
        st.dataframe(sample_requests, use_container_width=True)
    
    def predictive_analytics(self):
        st.header("🔮 Predictive Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            district = st.selectbox("Select District", ['Mumbai', 'Pune', 'Nagpur'])
            service_type = st.selectbox("Service Type", ['Health', 'Infrastructure', 'Safety'])
            
        with col2:
            month = st.slider("Month", 1, 12, datetime.now().month)
            
        if st.button("🎯 Generate AI Prediction"):
            # Simulate prediction using AI
            prediction_prompt = f"""
            Predict service demand for Maharashtra governance:
            
            District: {district}
            Service Type: {service_type}
            Month: {month}
            
            Provide:
            - Predicted number of requests
            - Key factors influencing demand
            - Resource requirements
            - Preventive measures
            
            Base prediction on typical patterns for Indian state governance.
            """
            
            try:
                response = self.model.generate_content(prediction_prompt)
                st.success("🤖 AI Prediction Generated!")
                st.markdown(response.text)
                
                # Generate forecast chart
                dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
                base_demand = 125
                forecast = [base_demand + (i * 2) + (i % 7 * 10) for i in range(30)]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=dates, y=forecast, mode='lines+markers', 
                                       name='Predicted Demand', line=dict(color='blue')))
                fig.update_layout(title=f"30-Day Demand Forecast: {service_type} in {district}")
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")
    
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
        
        fig_pie = px.pie(values=counts, names=categories, 
                        title="Service Requests by Category",
                        color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # AI-generated insights
        if st.button("🧠 Generate AI Insights"):
            insights_prompt = """
            Generate citizen service insights for Maharashtra governance based on typical patterns:
            
            Provide:
            1. Top 3 citizen concerns
            2. Service improvement recommendations
            3. Resource allocation suggestions
            4. Citizen engagement strategies
            
            Keep insights practical and actionable.
            """
            
            try:
                response = self.model.generate_content(insights_prompt)
                st.markdown("### 🎯 AI-Generated Insights:")
                st.info(response.text)
            except Exception as e:
                st.error(f"Insights generation failed: {str(e)}")

if __name__ == "__main__":
    dashboard = GovernanceDashboard()
    dashboard.run()