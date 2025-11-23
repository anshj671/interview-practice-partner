# Interview Practice Partner

An intelligent conversational AI agent designed to help users prepare for job interviews through realistic mock interview sessions. The agent conducts role-specific interviews, asks intelligent follow-up questions, and provides constructive feedback.

## Features

### Core Capabilities
- **Role-Specific Interviews**: Practice interviews for 5+ different roles (Software Engineer, Sales Representative, Retail Associate, Data Scientist, Product Manager)
- **Intelligent Follow-Up Questions**: The agent asks contextual follow-up questions based on your responses, just like a real interviewer
- **Comprehensive Feedback**: Receive detailed feedback on your responses including strengths, weaknesses, and actionable suggestions
- **Dual Interface Modes**: 
  - **Voice Interface** (Preferred): Natural voice-based conversation using speech recognition and text-to-speech
  - **Text Interface**: Traditional chat-based interaction

### Agentic Behavior
- **Adaptive Conversation**: Adapts to different user types (confused, efficient, chatty, normal)
- **Off-Topic Handling**: Gently redirects users back to interview topics when they go off-topic
- **Context Awareness**: Maintains conversation context to ask relevant follow-up questions
- **User Type Detection**: Automatically detects and adapts to user behavior patterns

### Edge Case Handling
The agent handles various edge cases including:
- **Confused Users**: Provides clear guidance and simplified instructions
- **Efficient Users**: Acknowledges brevity while encouraging elaboration
- **Chatty Users**: Gently redirects to stay on topic and be concise
- **Invalid Inputs**: Handles gibberish, special characters, and unclear input gracefully
- **Capability Requests**: Politely explains limitations (e.g., no video, no file uploads)

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for LLM capabilities)
- Microphone (for voice interface)

### Setup

1. **Clone or download the project**
```bash
cd interview_practice_partner
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
```

4. **Install system dependencies (for voice interface)**
   - **macOS**: `brew install portaudio`
   - **Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`
   - **Windows**: Usually included with PyAudio installation

## Usage

### Text Interface (Default)
```bash
python main.py --text
```
or simply:
```bash
python main.py
```

### Voice Interface
```bash
python main.py --voice
```

### Running Demo Scenarios
To see the agent handle different user types and edge cases:
```bash
python demo_scenarios.py
```

## Design Decisions

### Architecture

#### 1. **Modular Design**
The system is divided into focused modules:
- `interview_agent.py`: Core conversational agent logic
- `interview_roles.py`: Role configurations and question sets
- `feedback_analyzer.py`: Response evaluation and feedback generation
- `voice_interface.py`: Voice I/O handling
- `edge_case_handler.py`: Edge case detection and handling
- `main.py`: Entry point and UI orchestration

**Rationale**: This separation allows for easy maintenance, testing, and extension. Each module has a single responsibility.

#### 2. **LLM-Powered Follow-Up Questions**
Follow-up questions are generated dynamically using an LLM rather than using pre-written templates.

**Rationale**: 
- Enables more natural, contextual conversations
- Allows the agent to dig deeper into specific points mentioned by the candidate
- Creates a more realistic interview experience

#### 3. **Hybrid Feedback System**
The feedback system uses LLM analysis when available, with a rule-based fallback.

**Rationale**:
- LLM provides nuanced, contextual feedback
- Rule-based fallback ensures the system works even without API access
- Balances quality with reliability

#### 4. **User Type Detection**
The agent automatically detects user behavior patterns (confused, efficient, chatty) and adapts its responses.

**Rationale**:
- Improves user experience by adapting to individual needs
- Demonstrates intelligent, agentic behavior
- Handles edge cases proactively

#### 5. **Voice-First Design**
Voice interface is the preferred mode, with text as fallback.

**Rationale**:
- Voice is more natural for interview practice
- Better simulates real interview scenarios
- Aligns with assignment requirements (voice preferred)

### Conversation Quality

#### 1. **Natural Language Generation**
- Uses temperature=0.7 for LLM to balance consistency with naturalness
- Prompts are designed to generate conversational, not robotic, responses
- Follow-up questions are generated in real-time based on context

#### 2. **Context Management**
- Maintains conversation history for context-aware follow-ups
- Tracks interview state (questions asked, follow-up count, off-topic count)
- Uses recent context (last 3 exchanges) for evaluation

#### 3. **Error Recovery**
- Graceful handling of API failures with fallback mechanisms
- Clear error messages that guide users
- Doesn't penalize users for mistakes or confusion

### Agentic Behavior

#### 1. **Proactive Adaptation**
- Detects when responses are too brief and asks for elaboration
- Identifies off-topic responses and redirects politely
- Adjusts follow-up strategy based on response quality

#### 2. **State Management**
- Tracks interview progress, user type, and conversation flow
- Makes decisions about when to ask follow-ups vs. move to next question
- Manages interview lifecycle (start, in-progress, end)

#### 3. **Intelligent Decision Making**
- Uses multiple signals (response length, score, user type) to decide on follow-ups
- Balances interview flow with thoroughness
- Adapts to user needs (e.g., more guidance for confused users)

### Technical Implementation

#### 1. **Technology Stack**
- **LangChain**: For LLM orchestration and prompt management
- **OpenAI GPT-4o-mini**: For natural language understanding and generation
- **SpeechRecognition**: For voice input
- **pyttsx3**: For text-to-speech output
- **Python 3.8+**: Core language

**Rationale**: 
- LangChain provides abstraction for LLM operations
- GPT-4o-mini balances cost and quality
- Standard libraries for voice I/O

#### 2. **Configuration Management**
- Centralized configuration in `config.py`
- Environment variables for sensitive data (API keys)
- Easy customization of interview parameters

#### 3. **Error Handling**
- Try-except blocks around LLM calls with fallbacks
- Graceful degradation when voice interface unavailable
- Clear error messages for users

## Demo Scenarios

The project includes demo scenarios demonstrating different user types:

1. **The Confused User**: Shows how the agent provides guidance and clarification
2. **The Efficient User**: Demonstrates encouragement for elaboration
3. **The Chatty User**: Illustrates gentle redirection to stay on topic
4. **Edge Case Users**: Handles invalid inputs, capability requests, and errors
5. **Normal Interview Flow**: Shows standard interview progression

Run `python demo_scenarios.py` to see these in action.

## Evaluation Criteria Alignment

### Conversational Quality ✅
- Natural, flowing conversations with contextual follow-ups
- Adapts language and tone to user needs
- Handles interruptions and topic changes gracefully

### Agentic Behaviour ✅
- Proactively detects user type and adapts
- Makes intelligent decisions about follow-ups
- Maintains state and context throughout conversation
- Provides updates and feedback during the interview

### Technical Implementation ✅
- Clean, modular architecture
- Error handling and fallback mechanisms
- Voice and text interfaces
- LLM integration with proper prompt engineering

### Intelligence & Adaptability ✅
- User type detection and adaptation
- Context-aware follow-up questions
- Comprehensive feedback system
- Edge case handling

## Limitations & Future Improvements

### Current Limitations
1. **No video support**: Text/voice only
2. **No file uploads**: Cannot process resumes or documents
3. **Fixed question sets**: Questions are predefined per role (though follow-ups are dynamic)
4. **Single interview at a time**: Cannot compare multiple interviews

### Potential Improvements
1. **Multi-modal support**: Add video analysis for body language feedback
2. **Resume integration**: Parse resumes to customize questions
3. **Interview history**: Save and compare past interviews
4. **Custom roles**: Allow users to define custom interview roles
5. **Real-time feedback**: Provide feedback during the interview, not just at the end
6. **Performance analytics**: Track improvement over time

## Testing

### Manual Testing
Test the agent with different scenarios:
- Start an interview and answer questions naturally
- Try going off-topic to see redirection
- Give very brief answers to trigger follow-ups
- Test edge cases (invalid input, capability requests)

### Demo Scenarios
Run the included demo scenarios:
```bash
python demo_scenarios.py
```

## Troubleshooting

### Voice Interface Issues
- **Microphone not detected**: Check system microphone permissions
- **Speech not recognized**: Speak clearly and check internet connection (uses Google Speech Recognition)
- **TTS not working**: Install system TTS dependencies

### API Issues
- **OpenAI API errors**: Check API key in `.env` file
- **Rate limiting**: The system uses gpt-4o-mini which has higher rate limits
- **Fallback mode**: System will use rule-based analysis if LLM unavailable

## License

This project is created for educational/assignment purposes.

## Contact

For questions or issues, please refer to the code comments or documentation.

