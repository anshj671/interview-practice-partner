# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create a `.env` file:
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

### 3. Run the Application
```bash
python main.py
```

## 📝 Example Session

```
You: start interview software engineer

Interviewer: Hello! Welcome to your mock interview for the Software Engineer position...

Interviewer: Tell me about a challenging technical problem you've solved recently.

You: I once had to debug a memory leak in a production system...

Interviewer: That's interesting. Can you tell me more about your debugging process?

You: I used profiling tools to identify the issue...

[Interview continues...]

Interviewer: Thank you for completing the interview! Here's your feedback:
[Detailed feedback provided]
```

## 🎯 Try Different Modes

### Text Mode (Default)
```bash
python main.py --text
```

### Voice Mode
```bash
python main.py --voice
```

### Demo Scenarios
```bash
python demo_scenarios.py
```

## 💡 Tips

1. **Be Natural**: Answer questions as you would in a real interview
2. **Use Examples**: Provide specific examples from your experience
3. **Ask for Clarification**: If confused, the agent will help
4. **Practice Different Roles**: Try multiple roles to get varied practice

## 🆘 Need Help?

- Check `README.md` for detailed documentation
- See `SETUP.md` for troubleshooting
- Review `PROJECT_STRUCTURE.md` to understand the codebase

