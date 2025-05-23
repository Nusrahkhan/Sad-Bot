# Sad Bot

A fun web application that generates emotional replies and sobs as well based on user input. The bot uses AI to create personalized, humorous roasts and pairs them with reaction GIFs and voice responses.

## Features

- **Text-based Roasts**: Enter text about yourself and get a personalized roast
- **Voice Input**: Record your voice and have it transcribed using the Whisper model
- **Voice Responses**: Roasts are read aloud using ElevenLabs text-to-speech
- **Dark/Light Mode**: Toggle between dark and light themes
- **Model Selection**: Choose between different AI models for roasting

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   > **Note**: The speech recognition feature requires specific dependencies including TensorFlow and Keras. If you encounter any issues, make sure these are properly installed.

3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   ELEVEN_API_KEY=your_elevenlabs_api_key
   ```
4. Run the application:
   ```
   python roast_bot.py
   ```
Note: This was given as a task in a workshop to convert a sarcastic roast bot to emotional or funny bot.
