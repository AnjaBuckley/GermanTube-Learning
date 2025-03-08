

# GermanTube Learning

An application for English speakers to learn German through YouTube videos. The app fetches YouTube transcripts, generates interactive quizzes using AI, and tracks learning progress.

## Features

- Paste any German YouTube video URL
- Automatically fetch German transcripts
- Generate AI-powered quizzes based on video content
- Multiple quiz types: multiple choice, fill-in-the-blank, vocabulary
- Adjustable difficulty levels
- Track learning progress over time

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/germantube-learning.git
   cd germantube-learning
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   cp .env.example .env
   # Edit .env with your actual API key
   ```

### Running Locally

Start the Streamlit app: 
