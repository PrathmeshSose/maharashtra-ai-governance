import google.generativeai as genai
from google.cloud import bigquery
from datetime import datetime, timedelta
import json
from config import Config

class ServicePrioritizationEngine:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.bq_client = bigquery.Client(project=Config.PROJECT_ID)
        
    def analyze_citizen_query(self, query_text):
        """Use Gemini to analyze and categorize citizen queries"""
        prompt = f"""
        Analyze this citizen service request and provide:
        1. Service category (health, infrastructure, safety, education, other)
        2. Urgency level (low, medium, high, critical)
        3. Required department
        4. Estimated resolution time in days
        
        Query: {query_text}
        
        Respond in JSON format only.
        """
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except:
            return {
                "service_category": "other",
                "urgency_level": "medium", 
                "department": "general",
                "estimated_days": 7
            }
    
    def route_service_request(self, request_data):
        """Route service requests based on priority and capacity"""
        analysis = self.analyze_citizen_query(request_data['description'])
        
        # Calculate priority score
        priority_score = self._calculate_priority(
            analysis['urgency_level'],
            request_data.get('citizen_feedback_score', 3),
            analysis['estimated_days']
        )
        
        # Find best department based on capacity
        department = self._find_optimal_department(
            analysis['service_category'],
            analysis['department']
        )
        
        return {
            'request_id': request_data['id'],
            'assigned_department': department,
            'priority_score': priority_score,
            'estimated_resolution': analysis['estimated_days'],
            'service_category': analysis['service_category'],
            'routing_timestamp': datetime.now().isoformat()
        }
    
    def _calculate_priority(self, urgency, feedback_score, estimated_days):
        """Calculate dynamic priority score"""
        urgency_weights = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        
        base_score = urgency_weights.get(urgency, 2) * 25
        feedback_bonus = (feedback_score - 3) * 5  # Boost for high citizen ratings
        time_penalty = max(0, (estimated_days - 3) * 2)  # Penalty for long resolution
        
        return min(100, max(10, base_score + feedback_bonus - time_penalty))
    
    def _find_optimal_department(self, category, suggested_dept):
        """Find department with optimal capacity"""
        # Query current department workload
        query = f"""
        SELECT department, COUNT(*) as active_requests
        FROM `{Config.PROJECT_ID}.citizen_services.active_requests`
        WHERE status = 'pending'
        GROUP BY department
        ORDER BY active_requests ASC
        """
        
        try:
            results = self.bq_client.query(query).to_dataframe()
            if not results.empty:
                return results.iloc[0]['department']
        except:
            pass
            
        return suggested_dept
    
    def generate_summary_report(self, requests_data):
        """Generate executive summary using Gemini"""
        summary_prompt = f"""
        Generate an executive summary for Maharashtra governance dashboard:
        
        Data: {json.dumps(requests_data[:10])}  # Limit for token efficiency
        
        Include:
        - Key trends in citizen service requests
        - Top priority areas requiring attention
        - Resource allocation recommendations
        - 3 actionable insights for decision makers
        
        Keep response under 200 words.
        """
        
        response = self.model.generate_content(summary_prompt)
        return response.text