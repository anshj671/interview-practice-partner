"""
Main entry point for the Interview Practice Partner
Supports both voice and text interfaces
"""
import sys
import argparse
from colorama import init, Fore, Style
from interview_agent import InterviewAgent
from voice_interface import VoiceInterface
from config import VOICE_ENABLED, VOICE_LANGUAGE, VOICE_RATE

# Initialize colorama for colored terminal output
init(autoreset=True)

def print_colored(text: str, color: str = Fore.WHITE):
    """Print colored text"""
    print(f"{color}{text}{Style.RESET_ALL}")

def run_text_interface():
    """Run the interview agent with text-based interface"""
    agent = InterviewAgent(use_voice=False)
    
    print_colored("\n" + "="*60, Fore.CYAN)
    print_colored("  INTERVIEW PRACTICE PARTNER", Fore.CYAN)
    print_colored("="*60, Fore.CYAN)
    print_colored("\nWelcome! I'm your AI interview practice partner.", Fore.GREEN)
    print_colored("Type 'help' to see available commands.\n", Fore.YELLOW)
    
    # Show available roles
    roles = agent._list_available_roles()
    print_colored("Available roles:", Fore.CYAN)
    for role in roles:
        print_colored(f"  • {role.title()}", Fore.WHITE)
    print()
    
    while True:
        try:
            user_input = input(f"{Fore.BLUE}You: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
            
            response = agent.handle_user_input(user_input)
            print_colored(f"\n{Fore.MAGENTA}Interviewer: {Style.RESET_ALL}{response}\n")
            
            # Check if interview ended
            if "Thank you for completing" in response:
                continue_choice = input(f"{Fore.YELLOW}Start another interview? (y/n): {Style.RESET_ALL}").strip().lower()
                if continue_choice != 'y':
                    break
                print()
        
        except KeyboardInterrupt:
            print_colored("\n\nGoodbye! Thanks for practicing with me.", Fore.GREEN)
            break
        except EOFError:
            break

def run_voice_interface():
    """Run the interview agent with voice-based interface"""
    try:
        voice = VoiceInterface(language=VOICE_LANGUAGE, rate=VOICE_RATE)
        agent = InterviewAgent(use_voice=True)
    except Exception as e:
        print_colored(f"Error initializing voice interface: {e}", Fore.RED)
        print_colored("Falling back to text interface...", Fore.YELLOW)
        return run_text_interface()
    
    print_colored("\n" + "="*60, Fore.CYAN)
    print_colored("  INTERVIEW PRACTICE PARTNER (VOICE MODE)", Fore.CYAN)
    print_colored("="*60, Fore.CYAN)
    print_colored("\nVoice interface initialized!", Fore.GREEN)
    print_colored("Say 'start interview [role]' to begin.\n", Fore.YELLOW)
    
    # Initial greeting
    greeting = "Hello! I'm your AI interview practice partner. Say 'start interview' followed by a role name to begin."
    voice.speak(greeting)
    print_colored(f"Interviewer: {greeting}\n", Fore.MAGENTA)
    
    while True:
        try:
            # Listen for user input
            user_input = voice.listen(timeout=10, phrase_time_limit=30)
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "goodbye"]:
                goodbye = "Thank you for practicing with me. Goodbye!"
                voice.speak(goodbye)
                print_colored(f"\nInterviewer: {goodbye}\n", Fore.MAGENTA)
                break
            
            # Process input
            response = agent.handle_user_input(user_input)
            
            # Speak response
            voice.speak(response)
            print_colored(f"\nInterviewer: {response}\n", Fore.MAGENTA)
            
            # Check if interview ended
            if "Thank you for completing" in response:
                voice.speak("Would you like to practice another interview? Say yes or no.")
                continue_choice = voice.listen(timeout=10)
                if continue_choice and "no" in continue_choice.lower():
                    break
                print()
        
        except KeyboardInterrupt:
            goodbye = "Goodbye! Thanks for practicing with me."
            voice.speak(goodbye)
            print_colored(f"\n\n{goodbye}\n", Fore.GREEN)
            break

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Interview Practice Partner - AI-powered mock interview assistant"
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Use voice interface (default: text interface)"
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Use text interface (default)"
    )
    
    args = parser.parse_args()
    
    # Determine interface mode
    use_voice = args.voice or (VOICE_ENABLED and not args.text)
    
    if use_voice:
        run_voice_interface()
    else:
        run_text_interface()

if __name__ == "__main__":
    main()

