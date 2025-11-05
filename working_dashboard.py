import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json

class GovernanceDashboard:
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
            "Citizen Insights",
            "Security & Compliance"
        ])
        
        if page == "Executive Overview":
            self.executive_overview()
        elif page == "AI Service Engine":
            self.ai_service_engine()
        elif page == "Predictive Analytics":
            self.predictive_analytics()
        elif page == "Citizen Insights":
            self.citizen_insights()
        elif page == "Security & Compliance":
            self.security_compliance()
    
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
        
        # Real-time alerts
        st.subheader("🚨 Real-time Alerts")
        alerts = [
            {"type": "High Priority", "message": "Water shortage reported in Pune - 150 requests", "time": "2 min ago"},
            {"type": "Resource Alert", "message": "Health department capacity at 95% in Mumbai", "time": "5 min ago"},
            {"type": "Prediction", "message": "Infrastructure requests expected to increase 20% next week", "time": "10 min ago"}
        ]
        
        for alert in alerts:
            if alert["type"] == "High Priority":
                st.error(f"🔴 {alert['message']} - {alert['time']}")
            elif alert["type"] == "Resource Alert":
                st.warning(f"🟡 {alert['message']} - {alert['time']}")
            else:
                st.info(f"🔵 {alert['message']} - {alert['time']}")
    
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
                        # Simulate AI analysis
                        analysis = self.simulate_ai_analysis(citizen_query, district)
                        
                        st.success("✅ AI Analysis Complete!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### 🎯 AI Analysis Results:")
                            st.json(analysis)
                        
                        with col2:
                            st.markdown("### 📋 Routing Decision:")
                            routing = {
                                "assigned_department": analysis["department"],
                                "priority_score": analysis["priority_score"],
                                "estimated_resolution": f"{analysis['estimated_days']} days",
                                "officer_assigned": "Officer_" + str(hash(citizen_query) % 1000),
                                "citizen_message": f"Your {analysis['service_category']} request has been received and assigned to {analysis['department']}. Expected resolution: {analysis['estimated_days']} days."
                            }
                            st.json(routing)
        
        # Recent AI-processed requests
        st.subheader("📊 Recent AI-Processed Requests")
        sample_requests = pd.DataFrame({
            'Request ID': ['REQ_001', 'REQ_002', 'REQ_003', 'REQ_004', 'REQ_005'],
            'District': ['Mumbai', 'Pune', 'Nagpur', 'Mumbai', 'Nashik'],
            'Category': ['Health', 'Infrastructure', 'Safety', 'Education', 'Health'],
            'AI Priority Score': [92, 88, 85, 78, 95],
            'Status': ['Routed', 'In Progress', 'Resolved', 'Pending', 'Critical'],
            'AI Confidence': ['95%', '89%', '92%', '87%', '98%'],
            'Resolution Time': ['2 days', '5 days', '1 day', '7 days', '4 hours']
        })
        st.dataframe(sample_requests, use_container_width=True)
    
    def simulate_ai_analysis(self, query, district):
        """Simulate AI analysis based on keywords"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['water', 'supply', 'pipe', 'leak']):
            return {
                "service_category": "infrastructure",
                "urgency_level": "high",
                "department": "Water Supply Department",
                "estimated_days": 3,
                "priority_score": 85
            }
        elif any(word in query_lower for word in ['health', 'medical', 'hospital', 'doctor']):
            return {
                "service_category": "health",
                "urgency_level": "critical",
                "department": "Health Services",
                "estimated_days": 1,
                "priority_score": 95
            }
        elif any(word in query_lower for word in ['road', 'traffic', 'street', 'pothole']):
            return {
                "service_category": "infrastructure",
                "urgency_level": "medium",
                "department": "Public Works Department",
                "estimated_days": 7,
                "priority_score": 70
            }
        else:
            return {
                "service_category": "general",
                "urgency_level": "medium",
                "department": "General Administration",
                "estimated_days": 5,
                "priority_score": 60
            }
    
    def predictive_analytics(self):
        st.header("🔮 Predictive Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            district = st.selectbox("Select District", ['Mumbai', 'Pune', 'Nagpur'])
            service_type = st.selectbox("Service Type", ['Health', 'Infrastructure', 'Safety'])
            
        with col2:
            month = st.slider("Month", 1, 12, datetime.now().month)
            
        if st.button("🎯 Generate Prediction"):
            # Simulate prediction
            base_demand = {"Health": 150, "Infrastructure": 120, "Safety": 80}[service_type]
            district_multiplier = {"Mumbai": 1.5, "Pune": 1.2, "Nagpur": 1.0}[district]
            predicted_demand = int(base_demand * district_multiplier)
            
            st.success(f"🤖 Predicted demand for {service_type} in {district}: **{predicted_demand} requests**")
            
            # Generate forecast chart
            dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
            forecast = [predicted_demand + (i * 2) + (i % 7 * 10) for i in range(30)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=forecast, mode='lines+markers', 
                                   name='Predicted Demand', line=dict(color='blue')))
            fig.update_layout(title=f"30-Day Demand Forecast: {service_type} in {district}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Resource allocation recommendations
            st.subheader("📋 Resource Allocation Recommendations")
            recommendations = [
                f"Increase {service_type.lower()} staff by 15% in {district}",
                f"Allocate additional budget of ₹{predicted_demand * 5000:,} for {service_type.lower()} services",
                f"Setup mobile service units in high-demand areas of {district}",
                f"Implement preventive measures to reduce {service_type.lower()} service requests"
            ]
            
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
    
    def citizen_insights(self):
        st.header("👥 Citizen Insights")
        
        # Satisfaction trends
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        satisfaction = [3.8 + (i % 10) * 0.1 + (i % 3) * 0.05 for i in range(30)]
        
        fig = px.line(x=dates, y=satisfaction, title="Citizen Satisfaction Trend (30 Days)")
        fig.update_yaxis(range=[3.5, 4.5])
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Service category breakdown
            categories = ['Health', 'Infrastructure', 'Safety', 'Education', 'Other']
            counts = [35, 28, 20, 12, 5]
            
            fig_pie = px.pie(values=counts, names=categories, 
                            title="Service Requests by Category",
                            color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Response time by category
            response_data = pd.DataFrame({
                'Category': categories,
                'Avg Response Time (days)': [2.1, 5.3, 1.8, 7.2, 4.5],
                'Target (days)': [2, 5, 2, 7, 5]
            })
            
            fig_bar = px.bar(response_data, x='Category', y=['Avg Response Time (days)', 'Target (days)'],
                           title="Response Time vs Target", barmode='group')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Top citizen concerns
        st.subheader("🎯 Top Citizen Concerns")
        concerns = pd.DataFrame({
            'Concern': ['Water Supply Issues', 'Road Maintenance', 'Healthcare Access', 'Power Outages', 'Waste Management'],
            'Frequency': [450, 380, 290, 220, 180],
            'Trend': ['↑ +15%', '↓ -5%', '↑ +8%', '→ 0%', '↑ +12%']
        })
        st.dataframe(concerns, use_container_width=True)
    
    def security_compliance(self):
        st.header("🔒 Security & Compliance Monitor")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Data Privacy Score", "98%", "+2%")
        with col2:
            st.metric("Audit Compliance", "100%", "0%")
        with col3:
            st.metric("Access Violations", "0", "0")
        with col4:
            st.metric("Data Retention", "Active", "✅")
        
        # Security events
        st.subheader("🛡️ Security Events (Last 24 Hours)")
        security_events = pd.DataFrame({
            'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(5)],
            'Event Type': ['LOGIN_SUCCESS', 'DATA_ACCESS', 'QUERY_EXECUTE', 'REPORT_GENERATE', 'PII_ANONYMIZED'],
            'User': ['admin_001', 'analyst_002', 'officer_003', 'admin_001', 'system'],
            'Status': ['SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS'],
            'Risk Level': ['LOW', 'LOW', 'LOW', 'LOW', 'LOW']
        })
        st.dataframe(security_events, use_container_width=True)
        
        # Compliance metrics
        st.subheader("📋 Compliance Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            compliance_data = {
                'Data Retention Policy': '100%',
                'PII Anonymization': '98%',
                'Access Control': '100%',
                'Audit Logging': '100%',
                'Encryption': '95%'
            }
            
            for metric, score in compliance_data.items():
                st.metric(metric, score)
        
        with col2:
            # Data retention chart
            retention_data = pd.DataFrame({
                'Data Type': ['Citizen Requests', 'Audit Logs', 'Analytics Data', 'System Logs'],
                'Retention Period (Years)': [7, 10, 5, 3],
                'Current Storage (GB)': [1250, 890, 2100, 450]
            })
            
            fig = px.bar(retention_data, x='Data Type', y='Current Storage (GB)',
                        title="Data Storage by Type")
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    dashboard = GovernanceDashboard()
    dashboard.run()