"""
Edge case handling for different user types and scenarios
"""
from typing import Optional, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from interview_agent import InterviewAgent

class EdgeCaseHandler:
    """Handles edge cases and different user behavior patterns"""
    
    def __init__(self, agent: "InterviewAgent"):
        self.agent = agent
        self.user_type_history: List[str] = []
        self.invalid_input_count = 0
        self.capability_requests: List[str] = []
    
    def handle_confused_user(self, user_input: str) -> Optional[str]:
        """
        Handle confused user who is unsure what they want
        
        Strategies:
        - Provide clear guidance
        - Offer examples
        - Simplify instructions
        """
        confused_indicators = [
            "i don't know", "i'm not sure", "what do you mean",
            "can you explain", "i'm confused", "how does this work",
            "what should i do", "help me understand"
        ]
        
        if any(indicator in user_input.lower() for indicator in confused_indicators):
            self.agent.user_type = "confused"
            
            if not self.agent.interview_started:
                return """I understand this might be new to you. Let me explain:

I'm here to help you practice for job interviews. Here's how it works:

1. Choose a role you want to practice for (like 'software engineer' or 'sales representative')
2. I'll ask you interview questions for that role
3. You answer naturally, just like in a real interview
4. I'll ask follow-up questions to help you practice
5. At the end, I'll give you feedback on your answers

Would you like to try? Just say 'start interview' followed by a role name. For example: 'start interview software engineer'"""
            
            else:
                # During interview, confused about a question
                current_question = self.agent.questions_asked[-1] if self.agent.questions_asked else ""
                return f"""I understand this question might be unclear. Let me rephrase it:

{current_question}

Think of it this way: I'm asking about your experience and how you handle situations related to this role. 
There's no right or wrong answer - just share your thoughts and experiences. Would you like to try answering, or should I move to the next question?"""
        
        return None
    
    def handle_efficient_user(self, user_input: str) -> Optional[str]:
        """
        Handle efficient user who wants quick results
        
        Strategies:
        - Acknowledge brevity but encourage elaboration
        - Provide concise feedback
        - Skip unnecessary pleasantries
        """
        if self.agent.user_type == "efficient" and len(user_input.split()) < 20:
            # User gave a brief answer, encourage more detail
            return "That's a good start! To help you practice for real interviews, could you elaborate a bit more? Perhaps share a specific example or explain your thought process?"
        
        return None
    
    def handle_chatty_user(self, user_input: str) -> Optional[str]:
        """
        Handle chatty user who frequently goes off topic
        
        Strategies:
        - Gently redirect
        - Acknowledge their input but guide back
        - Set boundaries if needed
        """
        if len(user_input.split()) > 200:
            self.agent.user_type = "chatty"
            return "I appreciate your detailed response! However, in interviews, it's important to be concise and stay on topic. Could you summarize your main point in 2-3 sentences?"
        
        return None
    
    def handle_invalid_input(self, user_input: str) -> Optional[str]:
        """
        Handle invalid inputs (gibberish, non-text, etc.)
        
        Strategies:
        - Detect invalid input
        - Provide helpful error message
        - Don't penalize user
        """
        # Check for very short or non-meaningful input
        if len(user_input.strip()) < 2:
            self.invalid_input_count += 1
            if self.invalid_input_count >= 3:
                return "I'm having trouble understanding your input. Could you please type or speak more clearly? If you need help, type 'help'."
            return "I didn't catch that. Could you please repeat your answer?"
        
        # Check for only special characters
        if not any(c.isalnum() for c in user_input):
            self.invalid_input_count += 1
            return "I can only process text responses. Could you please provide your answer in words?"
        
        # Reset counter on valid input
        if len(user_input.strip()) > 2 and any(c.isalnum() for c in user_input):
            self.invalid_input_count = 0
        
        return None
    
    def handle_capability_request(self, user_input: str) -> Optional[str]:
        """
        Handle requests beyond bot's capabilities
        
        Strategies:
        - Acknowledge the request
        - Explain limitations
        - Suggest alternatives
        """
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
        """
        Main entry point for edge case handling
        Returns response if edge case detected, None otherwise
        """
        # Check in order of priority
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

