import streamlit as st
import os
import json
from datetime import datetime
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import openai
from database import init_db, save_quiz_result, get_user_history

# Set page configuration
st.set_page_config(page_title="GermanTube Learning", page_icon="🇩🇪", layout="wide")

# Initialize database
init_db()

try:
    # Try to get API key from environment or secrets
    if os.getenv("OPENAI_API_KEY"):
        openai_api_key = os.getenv("OPENAI_API_KEY")
    else:
        openai_api_key = st.secrets["openai"]["api_key"]

    # Set the API key directly on the openai module
    openai.api_key = openai_api_key

    # Initialize client with compatibility check
    try:
        # Try the newer client approach first
        client = openai.OpenAI(api_key=openai_api_key)
    except (TypeError, AttributeError):
        # Fall back to the older approach if needed
        client = openai
except Exception as e:
    st.error(f"Error initializing OpenAI client: {type(e).__name__}")
    st.error("Please check your OpenAI API key configuration.")
    st.stop()


def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    if "youtu.be" in youtube_url:
        return youtube_url.split("/")[-1].split("?")[0]
    elif "youtube.com/watch" in youtube_url:
        import urllib.parse as urlparse

        parsed_url = urlparse.urlparse(youtube_url)
        return urlparse.parse_qs(parsed_url.query)["v"][0]
    return None


def get_transcript(video_id):
    """Get the transcript of a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["de"])
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None


def generate_quiz(transcript, quiz_type="mixed", difficulty="intermediate"):
    """Generate a quiz based on the transcript using OpenAI."""
    if not transcript:
        return None

    # Limit transcript length to avoid token limits
    max_chars = 14000  # Adjust based on your OpenAI model
    if len(transcript) > max_chars:
        transcript = transcript[:max_chars]

    prompt = f"""
    You are a German language teacher. Create a quiz based on the following German transcript.
    The quiz is for {difficulty} level English speakers learning German.
    
    Quiz type: {quiz_type}
    
    For multiple choice questions, provide 4 options with one correct answer.
    For fill-in-the-blank questions, provide the sentence with a blank and the correct word.
    For vocabulary questions, ask about important words from the transcript.
    
    Format the quiz in JSON with the following structure:
    {{
        "questions": [
            {{
                "type": "multiple_choice",
                "question": "Question text in English",
                "context": "Related part from the transcript in German",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "explanation": "Explanation why this is correct"
            }},
            {{
                "type": "fill_in_blank",
                "question": "Complete this sentence: Der Mann ___ in das Haus.",
                "context": "Related part from the transcript in German",
                "correct_answer": "geht",
                "explanation": "Explanation of the grammar or vocabulary"
            }}
        ]
    }}
    
    Create 5 questions total, mixing different types if quiz_type is "mixed".
    
    Transcript:
    {transcript}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
        )

        quiz_json = response.choices[0].message.content
        # Extract JSON from the response if needed
        if "```json" in quiz_json:
            quiz_json = quiz_json.split("```json")[1].split("```")[0].strip()
        elif "```" in quiz_json:
            quiz_json = quiz_json.split("```")[1].split("```")[0].strip()

        return json.loads(quiz_json)
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        return None


def display_quiz(quiz_data):
    """Display the quiz in the Streamlit app."""
    if not quiz_data or "questions" not in quiz_data:
        st.error("Invalid quiz data")
        return None

    user_answers = []

    for i, q in enumerate(quiz_data["questions"]):
        st.subheader(f"Question {i + 1}")

        # Display context
        if "context" in q and q["context"]:
            with st.expander("Context (German)"):
                st.write(q["context"])

        # Display question
        st.write(q["question"])

        # Handle different question types
        if q["type"] == "multiple_choice":
            options = q["options"]
            answer = st.radio("Select your answer:", options, key=f"q{i}")
            user_answers.append(
                {
                    "question_idx": i,
                    "user_answer": answer,
                    "correct_answer": q["correct_answer"],
                }
            )

        elif q["type"] == "fill_in_blank":
            answer = st.text_input("Your answer:", key=f"q{i}")
            user_answers.append(
                {
                    "question_idx": i,
                    "user_answer": answer,
                    "correct_answer": q["correct_answer"],
                }
            )

        st.markdown("---")

    submit = st.button("Submit Quiz")

    if submit:
        score = 0
        results = []

        for i, ans in enumerate(user_answers):
            q = quiz_data["questions"][ans["question_idx"]]
            is_correct = ans["user_answer"].lower() == ans["correct_answer"].lower()

            if is_correct:
                score += 1

            results.append(
                {
                    "question": q["question"],
                    "user_answer": ans["user_answer"],
                    "correct_answer": ans["correct_answer"],
                    "is_correct": is_correct,
                    "explanation": q.get("explanation", ""),
                }
            )

        # Display results
        st.header("Quiz Results")
        st.subheader(f"Score: {score}/{len(user_answers)}")

        for i, res in enumerate(results):
            with st.expander(f"Question {i + 1} - {'✓' if res['is_correct'] else '✗'}"):
                st.write(f"**Question:** {res['question']}")
                st.write(f"**Your answer:** {res['user_answer']}")
                st.write(f"**Correct answer:** {res['correct_answer']}")
                if res["explanation"]:
                    st.write(f"**Explanation:** {res['explanation']}")

        # Save results to database
        video_id = st.session_state.get("current_video_id", "unknown")
        save_quiz_result(video_id, score, len(user_answers), results)

        st.success("Quiz completed! Results saved.")

        return score, len(user_answers)

    return None


def main():
    st.title("🇩🇪 GermanTube Learning")
    st.write("Learn German with YouTube videos and interactive quizzes!")

    # Sidebar for navigation
    page = st.sidebar.radio("Navigation", ["Home", "History"])

    if page == "Home":
        # Input for YouTube URL
        youtube_url = st.text_input("Enter a German YouTube video URL:")

        col1, col2 = st.columns(2)

        with col1:
            quiz_type = st.selectbox(
                "Quiz Type", ["mixed", "multiple_choice", "fill_in_blank", "vocabulary"]
            )

        with col2:
            difficulty = st.selectbox(
                "Difficulty Level", ["beginner", "intermediate", "advanced"]
            )

        if youtube_url:
            video_id = extract_video_id(youtube_url)

            if video_id:
                st.session_state["current_video_id"] = video_id

                # Display the video
                st.video(f"https://www.youtube.com/watch?v={video_id}")

                # Get transcript button
                if st.button("Generate Quiz"):
                    with st.spinner("Fetching transcript..."):
                        transcript = get_transcript(video_id)

                    if transcript:
                        with st.spinner("Generating quiz..."):
                            quiz_data = generate_quiz(transcript, quiz_type, difficulty)

                        if quiz_data:
                            st.session_state["current_quiz"] = quiz_data
                            st.success("Quiz generated successfully!")
                            st.rerun()

                # Display quiz if available
                if "current_quiz" in st.session_state:
                    display_quiz(st.session_state["current_quiz"])
            else:
                st.error("Invalid YouTube URL. Please enter a valid URL.")

    elif page == "History":
        st.header("Your Learning History")

        history = get_user_history()

        if history:
            # Convert to DataFrame for display
            df = pd.DataFrame(history)
            df["date"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
            df["score_percent"] = (df["score"] / df["total_questions"] * 100).round(1)

            # Display summary
            st.subheader("Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Quizzes", len(df))
            col2.metric("Average Score", f"{df['score_percent'].mean():.1f}%")
            col3.metric("Videos Studied", df["video_id"].nunique())

            # Display history table
            st.subheader("Quiz History")
            st.dataframe(
                df[["date", "video_id", "score", "total_questions", "score_percent"]],
                hide_index=True,
                column_config={
                    "date": "Date",
                    "video_id": "Video",
                    "score": "Score",
                    "total_questions": "Questions",
                    "score_percent": "Percentage",
                },
            )
        else:
            st.info("No quiz history yet. Complete some quizzes to see your progress!")


if __name__ == "__main__":
    main()
