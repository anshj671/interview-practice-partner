# Quick Setup Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Step 3: Run the Application

### Text Mode (Recommended for first-time use):
```bash
python main.py
```

### Voice Mode:
```bash
python main.py --voice
```

## Step 4: Try Demo Scenarios

See how the agent handles different user types:
```bash
python demo_scenarios.py
```

## Troubleshooting

### If voice doesn't work:
- Install system dependencies:
  - macOS: `brew install portaudio`
  - Linux: `sudo apt-get install portaudio19-dev`
- The app will automatically fall back to text mode

### If you get API errors:
- Check that your `.env` file has the correct API key
- Ensure you have credits in your OpenAI account
- The system will use rule-based fallback if API is unavailable

## First Interview

1. Start the app: `python main.py`
2. Type: `start interview software engineer`
3. Answer the questions naturally
4. Receive feedback at the end!

