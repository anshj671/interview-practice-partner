# Project Structure

```
interview_practice_partner/
│
├── main.py                 # Main entry point (text/voice interface)
├── interview_agent.py      # Core conversational AI agent
├── interview_roles.py      # Role configurations and questions
├── feedback_analyzer.py    # Response evaluation and feedback generation
├── voice_interface.py      # Voice I/O handling (speech recognition & TTS)
├── edge_case_handler.py    # Edge case detection and handling
├── demo_scenarios.py       # Demo scenarios for testing
├── config.py               # Configuration settings
│
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
│
├── README.md              # Comprehensive documentation
├── SETUP.md               # Quick setup guide
└── PROJECT_STRUCTURE.md   # This file
```

## Module Responsibilities

### Core Modules

**main.py**
- Entry point for the application
- Handles command-line arguments
- Orchestrates text/voice interfaces
- Manages user interaction loop

**interview_agent.py**
- Main conversational agent logic
- Manages interview state and flow
- Generates follow-up questions using LLM
- Handles user input and commands
- Integrates with feedback analyzer and edge case handler

**interview_roles.py**
- Defines interview role configurations
- Stores role-specific questions and evaluation criteria
- Provides role lookup functionality

**feedback_analyzer.py**
- Analyzes candidate responses
- Generates detailed feedback (strengths, weaknesses, suggestions)
- Calculates scores and evaluations
- Creates final interview summary

**voice_interface.py**
- Handles speech recognition (input)
- Manages text-to-speech (output)
- Provides continuous listening capabilities
- Falls back gracefully if voice unavailable

**edge_case_handler.py**
- Detects different user types (confused, efficient, chatty)
- Handles invalid inputs
- Manages capability requests
- Provides appropriate responses for edge cases

**demo_scenarios.py**
- Predefined test scenarios
- Demonstrates different user types
- Shows edge case handling
- Useful for testing and demos

**config.py**
- Centralized configuration
- Environment variable management
- Default settings

## Data Flow

1. **User Input** → `main.py` → `interview_agent.py`
2. **Edge Case Check** → `edge_case_handler.py` → Response or Continue
3. **Response Processing** → `interview_agent.py` → `feedback_analyzer.py`
4. **Follow-up Generation** → `interview_agent.py` → LLM → Response
5. **Feedback Generation** → `feedback_analyzer.py` → Summary
6. **Output** → `main.py` → Text/Voice Interface → User

## Key Design Patterns

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Dependency Injection**: LLM client can be injected for testing
3. **Strategy Pattern**: Different handlers for different user types
4. **State Management**: Interview state tracked in agent class
5. **Fallback Mechanisms**: Rule-based fallbacks when LLM unavailable

