
from typing import List, Dict, Optional, Any
from datetime import datetime
import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from interview_roles import InterviewRole, get_role
from feedback_analyzer import FeedbackAnalyzer, InterviewFeedback, ResponseEvaluation
from edge_case_handler import EdgeCaseHandler
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_FOLLOW_UPS, MAX_OFF_TOPIC_REDIRECTS

class InterviewAgent:
    
    
    def __init__(self, use_voice: bool = False, llm_client=None):
        self.use_voice = use_voice
        self.llm_client = llm_client or ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.7,
            api_key=OPENAI_API_KEY
        )
        self.feedback_analyzer = FeedbackAnalyzer(llm_client=self.llm_client)
        self.edge_case_handler = EdgeCaseHandler(self)
        
        self.current_role: Optional[InterviewRole] = None
        self.questions_asked: List[str] = []
        self.conversation_history: List[Dict[str, str]] = []
        self.follow_up_count: int = 0
        self.off_topic_count: int = 0
        self.current_question_index: int = 0
        self.interview_started: bool = False
        self.interview_feedback: Optional[InterviewFeedback] = None
        
        self.user_type: Optional[str] = None
        self.last_response_length: int = 0
        
    def start_interview(self, role_name: str) -> str:
        
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
        
        role_name = self.current_role.name
        greeting_templates = [
            f"Hello! Welcome to your mock interview for the {role_name} position. I'm excited to learn more about you. Let's begin with our first question.",
            f"Good to meet you! Today we'll be conducting a practice interview for the {role_name} role. I'll ask you some questions, and feel free to answer naturally. Ready?",
            f"Hi there! I'll be your interviewer today for the {role_name} position. This is a practice session, so take your time and be yourself. Shall we start?",
        ]
        return random.choice(greeting_templates)
    
    def get_next_question(self) -> str:
        
        if not self.current_role:
            return "Please start an interview first by selecting a role."
        
        if self.current_question_index >= len(self.current_role.core_questions):
            return self._end_interview()
        
        question = self.current_role.core_questions[self.current_question_index]
        self.questions_asked.append(question)
        self.current_question_index += 1
        self.follow_up_count = 0
        
        return question
    
    def process_response(
        self, 
        user_response: str,
        detect_user_type: bool = True
    ) -> str:
        
        if not self.interview_started:
            return "Please start an interview first by selecting a role."
        
        if detect_user_type:
            self._detect_user_type(user_response)
        
        is_off_topic = self._check_off_topic(user_response)
        
        if is_off_topic:
            self.off_topic_count += 1
            if self.off_topic_count >= MAX_OFF_TOPIC_REDIRECTS:
                return self._handle_excessive_off_topic()
            return self._redirect_to_topic(user_response)
        
        self.off_topic_count = 0
        
        current_question = self.questions_asked[-1] if self.questions_asked else "Initial question"
        self.conversation_history.append({
            "question": current_question,
            "response": user_response,
            "timestamp": datetime.now().isoformat()
        })
        
        evaluation = self.feedback_analyzer.analyze_response(
            question=current_question,
            response=user_response,
            role_config=self.current_role,
            context=self.conversation_history[-3:]
        )
        self.interview_feedback.add_evaluation(evaluation)
        
        should_follow_up = self._should_ask_follow_up(user_response, evaluation)
        
        if should_follow_up and self.follow_up_count < MAX_FOLLOW_UPS:
            self.follow_up_count += 1
            follow_up = self._generate_follow_up_question(user_response, current_question)
            self.questions_asked.append(follow_up)
            return follow_up
        else:
            self.follow_up_count = 0
            return self.get_next_question()
    
    def _detect_user_type(self, response: str):
        
        response_lower = response.lower()
        response_length = len(response.split())
        self.last_response_length = response_length
        
        confused_indicators = ["i don't know", "i'm not sure", "what do you mean", "can you explain", "i'm confused"]
        if any(indicator in response_lower for indicator in confused_indicators):
            self.user_type = "confused"
            return
        
        if response_length < 15 and self.user_type != "chatty":
            self.user_type = "efficient"
            return
        
        if response_length > 150 or self.off_topic_count > 0:
            self.user_type = "chatty"
            return
        
        if not self.user_type:
            self.user_type = "normal"
    
    def _check_off_topic(self, response: str) -> bool:
        
        if not self.questions_asked:
            return False
        
        current_question = self.questions_asked[-1]
        
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an interview evaluator. Determine if the candidate's response is relevant to the question asked. Reply with only 'YES' if relevant or 'NO' if off-topic."),
                ("human", "Question: {question}\nResponse: {response}\nIs this response relevant to the question?")
            ])
            
            chain = prompt | self.llm_client
            result = chain.invoke({
                "question": current_question,
                "response": response
            })
            
            return "NO" in result.content.upper()
        except Exception:
            question_keywords = set(current_question.lower().split())
            response_keywords = set(response.lower().split())
            overlap = len(question_keywords & response_keywords)
            return overlap < 2 and len(response.split()) > 20
    
    def _should_ask_follow_up(self, response: str, evaluation: ResponseEvaluation) -> bool:
        
        if self.follow_up_count >= 1:
            return False
        
        if len(response.strip()) < 3:
            return False
        
        word_count = len(response.split())
        if word_count < 20 and word_count > 2:
            return True
        
        if evaluation.score < 5.0 and word_count < 40:
            return True
        
        if self.user_type == "efficient" and word_count < 25:
            return True
        
        if random.random() < 0.2 and self.follow_up_count == 0 and word_count < 50 and word_count > 15:
            return True
        
        return False
    
    def _generate_follow_up_question(self, response: str, original_question: str) -> str:
        
        try:
            if len(response.split()) < 20:
                instruction = "The candidate gave a very brief response. Ask them to elaborate with more details and specific examples."
            elif self.user_type == "efficient":
                instruction = "The candidate is being efficient. Encourage them to provide more context and depth."
            else:
                instruction = "Ask a specific follow-up that digs deeper into something concrete they mentioned."
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an experienced interviewer conducting a mock interview. Generate a natural follow-up question based on the candidate's response. Be conversational and encouraging."),
                ("human", "Original Question: {original_question}\nCandidate's Response: {response}\nRole: {role_description}\nInstruction: {instruction}\nGenerate a follow-up question:")
            ])
            
            chain = prompt | self.llm_client
            result = chain.invoke({
                "original_question": original_question,
                "response": response,
                "role_description": self.current_role.description,
                "instruction": instruction
            })
            
            follow_up = result.content.strip()
            follow_up = follow_up.strip('"').strip("'")
            return follow_up
        except Exception as e:
            if len(response.split()) < 20:
                return "Could you elaborate more on that? I'd like to hear more details about your approach."
            
            fallback_follow_ups = [
                "Can you walk me through your specific process in more detail?",
                "What was the outcome of that approach?",
                "Can you give me a concrete example of how you applied that?",
                "What challenges did you face and how did you overcome them?",
            ]
            return random.choice(fallback_follow_ups)
    
    def _redirect_to_topic(self, response: str) -> str:
        
        redirects = [
            "I appreciate your response. Let's refocus on the question I asked earlier.",
            "That's an interesting point. To help you practice, let's stay on topic with the interview question.",
            "I understand, but let's get back to the question so we can make the most of this practice session.",
        ]
        
        redirect = random.choice(redirects)
        current_question = self.questions_asked[-1] if self.questions_asked else ""
        return f"{redirect}\n\n{current_question}"
    
    def _handle_excessive_off_topic(self) -> str:
        
        return "I notice we keep going off-topic. Let's try to focus on the interview questions. Would you like to continue, or should we end the session?" 
    
    def _end_interview(self) -> str:
        
        if not self.interview_feedback:
            return "Interview session not found."
        
        final_feedback = self.feedback_analyzer.generate_final_feedback(
            self.current_role.name if self.current_role else "Unknown",
            self.interview_feedback.start_time
        )
        
        summary = final_feedback.generate_summary()
        
        self.interview_started = False
        
        return f"Thank you for completing the interview!\n\n{summary}"
    
    def handle_user_input(self, user_input: str) -> str:
        
        user_input_lower = user_input.lower().strip()
        
        edge_response = self.edge_case_handler.process_edge_case(user_input)
        if edge_response:
            return edge_response
        
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
        
        if not self.interview_started:
            return "Please start an interview first. Type 'start interview [role]' or use the help command to see available roles."
        
        return self.process_response(user_input)
    
    def _list_available_roles(self) -> List[str]:
        
        from interview_roles import list_roles
        return list_roles()
    
    def _get_help_message(self) -> str:
        
        roles = self._list_available_roles()
        return f"""Available Commands:
  • start interview [role] - Begin a new interview session
  • quit/exit/end - End the current session
  • help - Show this message

Available Roles: {', '.join(roles)}

Example: 'start interview software engineer'"""

