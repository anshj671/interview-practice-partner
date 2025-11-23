"""
Feedback and evaluation system for interview responses
"""
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class ResponseEvaluation:
    """Evaluation of a single interview response"""
    question: str
    response: str
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    score: float = 0.0  # 0-10 scale
    criteria_scores: Dict[str, float] = field(default_factory=dict)

@dataclass
class InterviewFeedback:
    """Complete feedback for an interview session"""
    role: str
    start_time: datetime
    end_time: datetime
    total_questions: int
    evaluations: List[ResponseEvaluation] = field(default_factory=list)
    overall_strengths: List[str] = field(default_factory=list)
    overall_weaknesses: List[str] = field(default_factory=list)
    overall_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    
    def add_evaluation(self, evaluation: ResponseEvaluation):
        """Add an evaluation to the feedback"""
        self.evaluations.append(evaluation)
        self._update_overall_scores()
    
    def _update_overall_scores(self):
        """Recalculate overall scores based on individual evaluations"""
        if not self.evaluations:
            return
        
        self.overall_score = sum(eval.score for eval in self.evaluations) / len(self.evaluations)
        self.total_questions = len(self.evaluations)
    
    def generate_summary(self) -> str:
        """Generate a human-readable summary of the feedback"""
        duration = (self.end_time - self.start_time).total_seconds() / 60
        
        summary = f"""
{'='*60}
INTERVIEW FEEDBACK SUMMARY
{'='*60}

Role: {self.role}
Duration: {duration:.1f} minutes
Total Questions: {self.total_questions}
Overall Score: {self.overall_score:.1f}/10.0

OVERALL STRENGTHS:
"""
        for i, strength in enumerate(self.overall_strengths, 1):
            summary += f"  {i}. {strength}\n"
        
        summary += "\nAREAS FOR IMPROVEMENT:\n"
        for i, weakness in enumerate(self.overall_weaknesses, 1):
            summary += f"  {i}. {weakness}\n"
        
        summary += "\nRECOMMENDATIONS:\n"
        for i, rec in enumerate(self.recommendations, 1):
            summary += f"  {i}. {rec}\n"
        
        summary += f"\n{'='*60}\n"
        return summary

class FeedbackAnalyzer:
    """Analyzes interview responses and generates feedback"""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.feedback = None
    
    def analyze_response(
        self, 
        question: str, 
        response: str, 
        role_config: Any,
        context: List[Dict[str, str]] = None
    ) -> ResponseEvaluation:
        """
        Analyze a single response and provide evaluation
        
        Args:
            question: The interview question asked
            response: The candidate's response
            role_config: InterviewRole configuration
            context: Previous Q&A context for better evaluation
        
        Returns:
            ResponseEvaluation object with feedback
        """
        # Use LLM to analyze the response if available
        if self.llm_client:
            return self._llm_analyze(question, response, role_config, context)
        else:
            # Fallback to rule-based analysis
            return self._rule_based_analyze(question, response, role_config)
    
    def _llm_analyze(
        self, 
        question: str, 
        response: str, 
        role_config: Any,
        context: List[Dict[str, str]] = None
    ) -> ResponseEvaluation:
        """Use LLM to analyze response"""
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        
        if not isinstance(self.llm_client, ChatOpenAI):
            self.llm_client = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert interview evaluator. Analyze the candidate's response 
            and provide constructive feedback. Be specific and actionable.

            Evaluation Criteria:
            {criteria}

            Provide your analysis in JSON format with:
            - strengths: list of 2-3 specific strengths
            - weaknesses: list of 2-3 specific areas for improvement
            - suggestions: list of 2-3 actionable suggestions
            - score: numerical score from 0-10
            - criteria_scores: dict with scores for each criterion (0-10)
            """),
            ("human", """Question: {question}
            
            Response: {response}
            
            Please provide detailed feedback in JSON format.""")
        ])
        
        criteria_text = "\n".join([
            f"- {key}: {value}" 
            for key, value in role_config.evaluation_criteria.items()
        ])
        
        chain = prompt | self.llm_client
        try:
            result = chain.invoke({
                "question": question,
                "response": response,
                "criteria": criteria_text
            })
            
            # Parse LLM response (assuming JSON format)
            import json
            import re
            content = result.content
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                feedback_data = json.loads(json_match.group())
            else:
                # Fallback if JSON parsing fails
                return self._rule_based_analyze(question, response, role_config)
            
            return ResponseEvaluation(
                question=question,
                response=response,
                strengths=feedback_data.get("strengths", []),
                weaknesses=feedback_data.get("weaknesses", []),
                suggestions=feedback_data.get("suggestions", []),
                score=float(feedback_data.get("score", 5.0)),
                criteria_scores=feedback_data.get("criteria_scores", {})
            )
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            return self._rule_based_analyze(question, response, role_config)
    
    def _rule_based_analyze(
        self, 
        question: str, 
        response: str, 
        role_config: Any
    ) -> ResponseEvaluation:
        """Rule-based fallback analysis"""
        response_lower = response.lower()
        response_length = len(response.split())
        
        strengths = []
        weaknesses = []
        suggestions = []
        score = 5.0
        
        # Length analysis
        if response_length < 20:
            weaknesses.append("Response is too brief. Provide more detail and examples.")
            score -= 1.5
        elif response_length > 200:
            weaknesses.append("Response may be too lengthy. Consider being more concise.")
            score -= 0.5
        else:
            strengths.append("Appropriate response length with good detail.")
            score += 0.5
        
        # Structure analysis
        if any(word in response_lower for word in ["first", "then", "finally", "because", "example"]):
            strengths.append("Response shows good structure and organization.")
            score += 0.5
        else:
            weaknesses.append("Response could benefit from clearer structure (e.g., using examples, step-by-step explanation).")
            suggestions.append("Use the STAR method (Situation, Task, Action, Result) to structure your responses.")
        
        # Specificity
        if any(word in response_lower for word in ["i", "my", "we", "our"]):
            strengths.append("Response includes personal experience and examples.")
            score += 0.5
        else:
            weaknesses.append("Response lacks personal examples. Interviewers value specific experiences.")
            suggestions.append("Include specific examples from your experience to make your response more compelling.")
        
        # Confidence indicators
        if any(word in response_lower for word in ["i think", "maybe", "perhaps", "i guess"]):
            weaknesses.append("Response contains hedging language. Be more confident in your statements.")
            score -= 0.5
            suggestions.append("Use more confident language. Replace 'I think' with direct statements.")
        
        score = max(0.0, min(10.0, score))
        
        return ResponseEvaluation(
            question=question,
            response=response,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            score=score,
            criteria_scores={}
        )
    
    def generate_final_feedback(self, role: str, start_time: datetime) -> InterviewFeedback:
        """Generate final comprehensive feedback"""
        if not self.feedback:
            self.feedback = InterviewFeedback(
                role=role,
                start_time=start_time,
                end_time=datetime.now(),
                total_questions=0
            )
        
        self.feedback.end_time = datetime.now()
        
        # Aggregate strengths and weaknesses
        all_strengths = []
        all_weaknesses = []
        all_suggestions = []
        
        for eval in self.feedback.evaluations:
            all_strengths.extend(eval.strengths)
            all_weaknesses.extend(eval.weaknesses)
            all_suggestions.extend(eval.suggestions)
        
        # Find most common themes
        from collections import Counter
        strength_themes = Counter(all_strengths)
        weakness_themes = Counter(all_weaknesses)
        
        self.feedback.overall_strengths = [item[0] for item in strength_themes.most_common(3)]
        self.feedback.overall_weaknesses = [item[0] for item in weakness_themes.most_common(3)]
        self.feedback.recommendations = list(set(all_suggestions))[:5]
        
        return self.feedback

