
from typing import Optional, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from interview_agent import InterviewAgent

class EdgeCaseHandler:
    
    
    def __init__(self, agent: "InterviewAgent"):
        self.agent = agent
        self.user_type_history: List[str] = []
        self.invalid_input_count = 0
        self.capability_requests: List[str] = []
    
    def handle_confused_user(self, user_input: str) -> Optional[str]:
        
        confused_indicators = [
            "i don't know", "i'm not sure", "what do you mean",
            "can you explain", "i'm confused", "how does this work",
            "what should i do", "help me understand"
        ]
        
        if any(indicator in user_input.lower() for indicator in confused_indicators):
            self.agent.user_type = "confused"
            
            if not self.agent.interview_started:
                return 
            
            else:
                current_question = self.agent.questions_asked[-1] if self.agent.questions_asked else ""
                return f
        
        return None
    
    def handle_efficient_user(self, user_input: str) -> Optional[str]:
        
        return None
    
    def handle_chatty_user(self, user_input: str) -> Optional[str]:
        
        if len(user_input.split()) > 200:
            self.agent.user_type = "chatty"
            return "I appreciate your detailed response! However, in interviews, it's important to be concise and stay on topic. Could you summarize your main point in 2-3 sentences?"
        
        return None
    
    def handle_invalid_input(self, user_input: str) -> Optional[str]:
        
        if len(user_input.strip()) < 2:
            self.invalid_input_count += 1
            if self.invalid_input_count >= 3:
                return "I'm having trouble understanding your input. Could you please type more clearly? If you need help, type 'help'. To move to the next question, I'll continue..."
            return "I didn't catch that. Could you please repeat your answer?"
        
        if not any(c.isalpha() for c in user_input):
            self.invalid_input_count += 1
            return "I can only process text responses. Could you please provide your answer in words?"
        
        words = user_input.split()
        if len(words) > 0 and len(user_input) > 5:
            vowel_count = sum(1 for c in user_input.lower() if c in 'aeiou')
            if vowel_count < len(user_input) * 0.1:
                self.invalid_input_count += 1
                if self.invalid_input_count >= 2:
                    return "I'm having trouble understanding. If you'd like to skip this question or need help, just let me know. Otherwise, please provide a clear answer."
                return "That doesn't seem like a complete answer. Could you please try again?"
        
        if len(user_input.strip()) > 2 and any(c.isalpha() for c in user_input):
            self.invalid_input_count = 0
        
        return None
    
    def handle_capability_request(self, user_input: str) -> Optional[str]:
        
        capability_keywords = {
            "video": ["video", "camera", "see me", "visual"],
            "file": ["upload", "file", "document", "resume", "cv"],
            "multiple": ["multiple roles", "compare", "different roles"],
            "custom": ["custom question", "my own question", "add question"],
        }
        
        user_lower = user_input.lower()
        for capability, keywords in capability_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                self.capability_requests.append(capability)
                
                responses = {
                    "video": "I don't support video interviews, but I can conduct voice or text-based interviews. Would you like to continue?",
                    "file": "I can't process file uploads, but you can describe your experience in your answers. That's actually great practice for verbal communication in interviews!",
                    "multiple": "I can conduct one interview at a time. After we finish this one, you can start a new interview for a different role. Would you like to continue?",
                    "custom": "I use role-specific questions to give you realistic practice. However, you can mention specific topics you'd like to discuss in your answers, and I'll ask follow-ups. Sound good?",
                }
                
                return responses.get(capability, "I understand your request, but that's not something I can do right now. I'm focused on conducting mock interviews with role-specific questions. Is there something else I can help you with?")
        
        return None
    
    def process_edge_case(self, user_input: str) -> Optional[str]:
        
        handlers = [
            self.handle_capability_request,
            self.handle_invalid_input,
            self.handle_confused_user,
            self.handle_efficient_user,
            self.handle_chatty_user,
        ]
        
        for handler in handlers:
            response = handler(user_input)
            if response:
                return response
        
        return None

