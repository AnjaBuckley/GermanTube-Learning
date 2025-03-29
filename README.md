

# GermanTube Learning

An application for English speakers to learn German through YouTube videos. The app fetches YouTube transcripts, generates interactive quizzes using AI, and tracks learning progress.

<img width="1106" alt="Screenshot 2025-03-29 at 16 15 59" src="https://github.com/user-attachments/assets/a3074d11-f01a-4ef3-a37b-469392d545d0" />
<img width="1140" alt="Screenshot 2025-03-29 at 16 16 12" src="https://github.com/user-attachments/assets/0fdc26bb-5164-4010-9850-9f53a7774bea" />
<img width="1112" alt="Screenshot 2025-03-29 at 16 16 23" src="https://github.com/user-attachments/assets/37598a73-925c-4979-86b5-4a386e33ac35" />
<img width="1123" alt="Screenshot 2025-03-29 at 16 17 30" src="https://github.com/user-attachments/assets/f9dbecf7-38d8-4d6c-89a2-1b442fe2ab30" />


## Live Demo

Try the app live at: [https://germantube.streamlit.app/](https://germantube.streamlit.app/)

## Features

- Paste any German YouTube video URL
- Automatically fetch German transcripts
- Generate AI-powered quizzes based on video content
- Multiple quiz types: multiple choice, fill-in-the-blank, vocabulary
- Adjustable difficulty levels (beginner, intermediate, advanced)
- Track learning progress over time

## How to Use

1. Visit [https://germantube.streamlit.app/](https://germantube.streamlit.app/)
2. Paste a German YouTube video URL in the input field
3. Select your preferred quiz type and difficulty level
4. Click "Generate Quiz"
5. Complete the quiz and submit to see your results
6. View your learning history in the History tab

## Getting Started (Local Development)

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/AnjaBuckley/GermanTube-Learning.git
   cd GermanTube-Learning
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
```
streamlit run app.py
```

## Deployment

The app is deployed using Streamlit Cloud. For your own deployment:

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app pointing to your forked repository
4. Add your OpenAI API key in the Streamlit Cloud secrets:
   ```toml
   [openai]
   api_key = "your-actual-openai-api-key"
   ```

## Technical Details

### Architecture

- **Frontend**: Streamlit for the user interface
- **APIs**: 
  - YouTube Transcript API for fetching video transcripts
  - OpenAI API for generating quizzes
- **Database**: SQLite for storing user quiz results
- **Deployment**: Streamlit Cloud

### Files

- `app.py`: Main Streamlit application
- `database.py`: Database operations
- `requirements.txt`: Project dependencies
- `.env.example`: Template for environment variables

## Future Enhancements

- User authentication
- More quiz types (listening comprehension, pronunciation)
- Spaced repetition for vocabulary learning
- Progress tracking with visualizations
- Video recommendations based on skill level

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT 
