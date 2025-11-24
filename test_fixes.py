"""
Quick test to verify the fixes work correctly
"""
from interview_agent import InterviewAgent

def test_interview_flow():
    """Test that interview doesn't repeat follow-ups"""
    print("Testing interview flow...")
    agent = InterviewAgent(use_voice=False)
    
    # Start interview
    response = agent.handle_user_input("start interview software engineer")
    print(f"Start: {response[:100]}...")
    
    # First response
    response = agent.handle_user_input("yes")
    print(f"\nFirst question: {response[:100]}...")
    
    # Brief response to trigger follow-up
    response = agent.handle_user_input("I used Python for data analysis")
    print(f"\nAfter brief answer: {response[:100]}...")
    
    # Another response (should NOT repeat the same follow-up)
    response = agent.handle_user_input("I worked on a machine learning project")
    print(f"\nAfter second answer: {response[:100]}...")
    
    # Check if it moved to next question or asked different follow-up
    if "That's a good start!" in response and agent.follow_up_count > 1:
        print("\n❌ FAILED: Still repeating follow-ups")
        return False
    else:
        print("\n✅ PASSED: Follow-ups working correctly")
        return True

if __name__ == "__main__":
    test_interview_flow()
