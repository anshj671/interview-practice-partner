"""
Demo scenarios for testing different user types and edge cases
"""
from typing import List, Dict, Tuple
from interview_agent import InterviewAgent
from edge_case_handler import EdgeCaseHandler

class DemoScenarios:
    """Predefined demo scenarios for testing"""
    
    def __init__(self):
        self.agent = InterviewAgent(use_voice=False)
        self.edge_case_handler = EdgeCaseHandler(self.agent)
    
    def run_confused_user_scenario(self):
        """Demo: The Confused User"""
        print("\n" + "="*60)
        print("DEMO SCENARIO: The Confused User")
        print("="*60 + "\n")
        
        scenarios = [
            ("User", "I don't know what to do"),
            ("User", "What is this? How does it work?"),
            ("User", "start interview"),
            ("User", "I'm not sure how to answer that"),
        ]
        
        self._run_scenario(scenarios)
    
    def run_efficient_user_scenario(self):
        """Demo: The Efficient User"""
        print("\n" + "="*60)
        print("DEMO SCENARIO: The Efficient User")
        print("="*60 + "\n")
        
        self.agent.start_interview("software engineer")
        question = self.agent.get_next_question()
        print(f"Interviewer: {question}\n")
        
        scenarios = [
            ("User", "I debug by checking logs."),
            ("User", "I use Git."),
            ("User", "I write tests."),
        ]
        
        self._run_scenario(scenarios)
    
    def run_chatty_user_scenario(self):
        """Demo: The Chatty User"""
        print("\n" + "="*60)
        print("DEMO SCENARIO: The Chatty User")
        print("="*60 + "\n")
        
        self.agent.start_interview("sales representative")
        question = self.agent.get_next_question()
        print(f"Interviewer: {question}\n")
        
        long_response = """Well, that's a great question! You know, I've been in sales for a while now, 
        and I remember this one time when I was working at this company, and we had this really difficult client, 
        and actually, that reminds me of another story about my friend who works in marketing, 
        and he told me about this campaign they ran, which was really interesting because it involved 
        social media and all that, and I think social media is really important these days, 
        don't you? I mean, everyone is on Instagram and TikTok now, and I actually have this really 
        funny story about TikTok that happened to me last week..."""
        
        scenarios = [
            ("User", long_response),
            ("User", "Oh, and also, I wanted to mention that I love cooking, and cooking is kind of like sales in a way, right?"),
        ]
        
        self._run_scenario(scenarios)
    
    def run_edge_case_scenario(self):
        """Demo: Edge Case Users"""
        print("\n" + "="*60)
        print("DEMO SCENARIO: Edge Case Users")
        print("="*60 + "\n")
        
        scenarios = [
            ("User", "Can I upload my resume?"),
            ("User", "Do you support video interviews?"),
            ("User", "???"),
            ("User", "a"),
            ("User", "start interview invalid_role_xyz"),
            ("User", "start interview software engineer"),
            ("User", "I want custom questions about my specific experience"),
        ]
        
        self._run_scenario(scenarios)
    
    def run_normal_interview_scenario(self):
        """Demo: Normal Interview Flow"""
        print("\n" + "="*60)
        print("DEMO SCENARIO: Normal Interview Flow")
        print("="*60 + "\n")
        
        self.agent.start_interview("retail associate")
        question = self.agent.get_next_question()
        print(f"Interviewer: {question}\n")
        
        scenarios = [
            ("User", "I would listen carefully to understand their concern, apologize for the inconvenience, and offer a solution like a replacement or refund."),
            ("User", "I once had a customer who received a damaged item. I immediately apologized, processed a full refund, and offered to help them find a replacement. They were very happy with the resolution."),
        ]
        
        self._run_scenario(scenarios)
    
    def _run_scenario(self, scenarios: List[Tuple[str, str]]):
        """Run a scenario with predefined inputs"""
        for speaker, text in scenarios:
            print(f"{speaker}: {text}\n")
            
            # Check for edge cases first
            edge_response = self.edge_case_handler.process_edge_case(text)
            if edge_response:
                print(f"Interviewer: {edge_response}\n")
            else:
                # Process normally
                if text.startswith("start interview"):
                    role = text.replace("start interview", "").strip()
                    if role:
                        response = self.agent.start_interview(role)
                    else:
                        response = self.agent.handle_user_input(text)
                else:
                    response = self.agent.handle_user_input(text)
                
                print(f"Interviewer: {response}\n")
            
            # Small delay for readability
            import time
            time.sleep(0.5)

def run_all_demos():
    """Run all demo scenarios"""
    demos = DemoScenarios()
    
    print("\n" + "="*70)
    print("  INTERVIEW PRACTICE PARTNER - DEMO SCENARIOS")
    print("="*70)
    
    demos.run_confused_user_scenario()
    print("\n" + "-"*60 + "\n")
    
    demos = DemoScenarios()  # Reset
    demos.run_efficient_user_scenario()
    print("\n" + "-"*60 + "\n")
    
    demos = DemoScenarios()  # Reset
    demos.run_chatty_user_scenario()
    print("\n" + "-"*60 + "\n")
    
    demos = DemoScenarios()  # Reset
    demos.run_edge_case_scenario()
    print("\n" + "-"*60 + "\n")
    
    demos = DemoScenarios()  # Reset
    demos.run_normal_interview_scenario()
    
    print("\n" + "="*70)
    print("  DEMO SCENARIOS COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_all_demos()

