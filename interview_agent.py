"""
Main conversational AI agent for conducting mock interviews
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
import random
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from interview_roles import InterviewRole, get_role
from feedback_analyzer import FeedbackAnalyzer, InterviewFeedback, ResponseEvaluation
from edge_case_handler import EdgeCaseHandler
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_FOLLOW_UPS, MAX_OFF_TOPIC_REDIRECTS

class InterviewAgent:
    """
    Conversational AI agent that conducts mock interviews with intelligent
    follow-up questions and adaptive behavior
    """
    
    def __init__(self, use_voice: bool = False, llm_client=None):
        self.use_voice = use_voice
        self.llm_client = llm_client or ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.7,
            api_key=OPENAI_API_KEY
        )
        self.feedback_analyzer = FeedbackAnalyzer(llm_client=self.llm_client)
        self.edge_case_handler = EdgeCaseHandler(self)
        
        # Interview state
        self.current_role: Optional[InterviewRole] = None
        self.questions_asked: List[str] = []
        self.conversation_history: List[Dict[str, str]] = []
        self.follow_up_count: int = 0
        self.off_topic_count: int = 0
        self.current_question_index: int = 0
        self.interview_started: bool = False
        self.interview_feedback: Optional[InterviewFeedback] = None
        
        # User behavior tracking
        self.user_type: Optional[str] = None  # confused, efficient, chatty, normal
        self.last_response_length: int = 0
        
    def start_interview(self, role_name: str) -> str:
        """Initialize and start a new interview session"""
        try:
            self.current_role = get_role(role_name)
            self.interview_started = True
            self.questions_asked = []
            self.conversation_history = []
            self.follow_up_count = 0
            self.off_topic_count = 0
            self.current_question_index = 0
            
            self.interview_feedback = InterviewFeedback(
                role=role_name,
                start_time=datetime.now(),
                end_time=datetime.now(),
                total_questions=0
            )
            self.feedback_analyzer.feedback = self.interview_feedback
            
            greeting = self._generate_greeting()
            return greeting
        except ValueError as e:
            return str(e)
    
    def _generate_greeting(self) -> str:
        """Generate a personalized greeting for the interview"""
        role_name = self.current_role.name
        greeting_templates = [
            f"Hello! Welcome to your mock interview for the {role_name} position. I'm excited to learn more about you. Let's begin with our first question.",
            f"Good to meet you! Today we'll be conducting a practice interview for the {role_name} role. I'll ask you some questions, and feel free to answer naturally. Ready?",
            f"Hi there! I'll be your interviewer today for the {role_name} position. This is a practice session, so take your time and be yourself. Shall we start?",
        ]
        return random.choice(greeting_templates)
    
    def get_next_question(self) -> str:
        """Get the next interview question"""
        if not self.current_role:
            return "Please start an interview first by selecting a role."
        
        if self.current_question_index >= len(self.current_role.core_questions):
            return self._end_interview()
        
        question = self.current_role.core_questions[self.current_question_index]
        self.questions_asked.append(question)
        self.current_question_index += 1
        self.follow_up_count = 0  # Reset follow-up counter for new question
        
        return question
    
    def process_response(
        self, 
        user_response: str,
        detect_user_type: bool = True
    ) -> str:
        """
        Process user's response and determine next action
        
        Args:
            user_response: The candidate's response
            detect_user_type: Whether to detect and adapt to user behavior type
        
        Returns:
            Next question or feedback message
        """
        if not self.interview_started:
            return "Please start an interview first by selecting a role."
        
        # Detect user type if enabled
        if detect_user_type:
            self._detect_user_type(user_response)
        
        # Check if response is off-topic
        is_off_topic = self._check_off_topic(user_response)
        
        if is_off_topic:
            self.off_topic_count += 1
            if self.off_topic_count >= MAX_OFF_TOPIC_REDIRECTS:
                return self._handle_excessive_off_topic()
            return self._redirect_to_topic(user_response)
        
        # Reset off-topic counter if on-topic
        self.off_topic_count = 0
        
        # Store conversation
        current_question = self.questions_asked[-1] if self.questions_asked else "Initial question"
        self.conversation_history.append({
            "question": current_question,
            "response": user_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Analyze response
        evaluation = self.feedback_analyzer.analyze_response(
            question=current_question,
            response=user_response,
            role_config=self.current_role,
            context=self.conversation_history[-3:]  # Last 3 exchanges for context
        )
        self.interview_feedback.add_evaluation(evaluation)
        
        # Determine if we should ask a follow-up
        should_follow_up = self._should_ask_follow_up(user_response, evaluation)
        
        if should_follow_up and self.follow_up_count < MAX_FOLLOW_UPS:
            self.follow_up_count += 1
            return self._generate_follow_up_question(user_response, current_question)
        else:
            # Move to next question
            return self.get_next_question()
    
    def _detect_user_type(self, response: str):
        """Detect user behavior type based on response patterns"""
        response_lower = response.lower()
        response_length = len(response.split())
        self.last_response_length = response_length
        
        # Confused user indicators
        confused_indicators = ["i don't know", "i'm not sure", "what do you mean", "can you explain", "i'm confused"]
        if any(indicator in response_lower for indicator in confused_indicators):
            self.user_type = "confused"
            return
        
        # Efficient user indicators (very brief responses)
        if response_length < 15 and self.user_type != "chatty":
            self.user_type = "efficient"
            return
        
        # Chatty user indicators (very long responses, off-topic tangents)
        if response_length > 150 or self.off_topic_count > 0:
            self.user_type = "chatty"
            return
        
        # Normal user (default)
        if not self.user_type:
            self.user_type = "normal"
    
    def _check_off_topic(self, response: str) -> bool:
        """Check if response is significantly off-topic"""
        if not self.questions_asked:
            return False
        
        current_question = self.questions_asked[-1]
        
        # Use LLM to check relevance
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are analyzing if a candidate's response is relevant to the interview question.
                Respond with only "YES" if the response is relevant/on-topic, or "NO" if it's clearly off-topic.
                Be lenient - only mark as off-topic if it's completely unrelated."""),
                ("human", """Question: {question}
                
                Response: {response}
                
                Is this response relevant to the question? (YES/NO)""")
            ])
            
            chain = prompt | self.llm_client
            result = chain.invoke({
                "question": current_question,
                "response": response
            })
            
            return "NO" in result.content.upper()
        except Exception:
            # Fallback: simple keyword-based check
            question_keywords = set(current_question.lower().split())
            response_keywords = set(response.lower().split())
            overlap = len(question_keywords & response_keywords)
            return overlap < 2 and len(response.split()) > 20
    
    def _should_ask_follow_up(self, response: str, evaluation: ResponseEvaluation) -> bool:
        """Determine if a follow-up question should be asked"""
        # Ask follow-up if response is too brief
        if len(response.split()) < 30:
            return True
        
        # Ask follow-up if response lacks specificity
        if evaluation.score < 6.0:
            return True
        
        # Ask follow-up if user type is "efficient" (to encourage elaboration)
        if self.user_type == "efficient":
            return True
        
        # Random chance for natural conversation flow
        if random.random() < 0.3 and self.follow_up_count == 0:
            return True
        
        return False
    
    def _generate_follow_up_question(self, response: str, original_question: str) -> str:
        """Generate a contextual follow-up question using LLM"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an interviewer conducting a mock interview. Generate a natural, 
                conversational follow-up question based on the candidate's response. The question should:
                1. Dig deeper into something they mentioned
                2. Ask for more specific details or examples
                3. Be relevant to the role: {role_description}
                4. Sound natural and conversational (not robotic)
                
                Keep it brief (one sentence). Don't repeat the original question."""),
                ("human", """Original Question: {original_question}
                
                Candidate's Response: {response}
                
                Generate a follow-up question:""")
            ])
            
            chain = prompt | self.llm_client
            result = chain.invoke({
                "original_question": original_question,
                "response": response,
                "role_description": self.current_role.description
            })
            
            follow_up = result.content.strip()
            # Remove quotes if present
            follow_up = follow_up.strip('"').strip("'")
            return follow_up
        except Exception as e:
            # Fallback follow-up questions
            fallback_follow_ups = [
                "Can you tell me more about that?",
                "That's interesting. Can you give me a specific example?",
                "How did that situation turn out?",
                "What did you learn from that experience?",
            ]
            return random.choice(fallback_follow_ups)
    
    def _redirect_to_topic(self, response: str) -> str:
        """Politely redirect user back to the interview topic"""
        redirects = [
            "I appreciate your response. Let's refocus on the question I asked earlier.",
            "That's an interesting point. To help you practice, let's stay on topic with the interview question.",
            "I understand, but let's get back to the question so we can make the most of this practice session.",
        ]
        
        redirect = random.choice(redirects)
        current_question = self.questions_asked[-1] if self.questions_asked else ""
        return f"{redirect}\n\n{current_question}"
    
    def _handle_excessive_off_topic(self) -> str:
        """Handle when user goes off-topic too many times"""
        return """I notice we've gone off-topic a few times. In a real interview, staying focused on the question is important. 
        Let's try to answer the question directly. Would you like me to rephrase the current question, or would you prefer to move to the next one?"""
    
    def _end_interview(self) -> str:
        """End the interview and provide feedback"""
        if not self.interview_feedback:
            return "Interview session not found."
        
        final_feedback = self.feedback_analyzer.generate_final_feedback(
            self.current_role.name if self.current_role else "Unknown",
            self.interview_feedback.start_time
        )
        
        summary = final_feedback.generate_summary()
        
        # Reset interview state
        self.interview_started = False
        
        return f"""Thank you for completing the interview! Here's your feedback:

{summary}

Would you like to practice another interview or review specific questions?"""
    
    def handle_user_input(self, user_input: str) -> str:
        """
        Main entry point for processing user input
        Handles both interview responses and commands
        """
        user_input_lower = user_input.lower().strip()
        
        # Check for edge cases first
        edge_response = self.edge_case_handler.process_edge_case(user_input)
        if edge_response:
            return edge_response
        
        # Handle commands
        if user_input_lower in ["quit", "exit", "end"]:
            if self.interview_started:
                return self._end_interview()
            return "Goodbye! Thanks for practicing with me."
        
        if user_input_lower in ["help", "commands"]:
            return self._get_help_message()
        
        if user_input_lower.startswith("start interview"):
            role = user_input_lower.replace("start interview", "").strip()
            if not role:
                return "Please specify a role. Available roles: " + ", ".join(self._list_available_roles())
            try:
                return self.start_interview(role)
            except ValueError as e:
                return str(e) + " Available roles: " + ", ".join(self._list_available_roles())
        
        # If interview hasn't started, prompt to start
        if not self.interview_started:
            return "Please start an interview first. Type 'start interview [role]' or use the help command to see available roles."
        
        # Process as interview response
        return self.process_response(user_input)
    
    def _list_available_roles(self) -> List[str]:
        """Get list of available interview roles"""
        from interview_roles import list_roles
        return list_roles()
    
    def _get_help_message(self) -> str:
        """Get help message with available commands"""
        roles = self._list_available_roles()
        return f"""
Available Commands:
- start interview [role] - Start a new interview (e.g., 'start interview software engineer')
- quit/exit - End the current interview
- help - Show this message

Available Roles:
{chr(10).join(f'  - {role}' for role in roles)}

During the interview, just answer the questions naturally. I'll ask follow-up questions to help you practice!
"""

