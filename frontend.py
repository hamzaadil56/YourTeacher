"""
AI Learning Companion - Multi-Agent Tutor MVP
A modern Streamlit application for personalized learning
"""

import streamlit as st
import time
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="AI Learning Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark theme styling


def load_css():
    st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
    }
    
    /* Custom Card Styles */
    .custom-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Hero Section Styles */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #a0a0c0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero-description {
        font-size: 1.1rem;
        color: #c0c0d0;
        text-align: center;
        max-width: 800px;
        margin: 0 auto 3rem;
        line-height: 1.6;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
    }
    
    /* Chat Message Styles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        margin: 0.5rem 0;
        padding: 1rem;
    }
    
    /* File Uploader Styles */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        border: 2px dashed rgba(102, 126, 234, 0.5);
    }
    
    /* Radio Button Styles */
    .stRadio > label {
        color: #c0c0d0;
        font-size: 1.1rem;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: rgba(15, 15, 30, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Progress Bar Styles */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metric Card Styles */
    .metric-card {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0c0;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state


def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'hero'
    if 'student_profile' not in st.session_state:
        st.session_state.student_profile = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'learning_topic' not in st.session_state:
        st.session_state.learning_topic = ""
    if 'screener_step' not in st.session_state:
        st.session_state.screener_step = 0
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}

# Hero Page


def hero_page():
    st.markdown('<h1 class="hero-title">AI Learning Companion</h1>',
                unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Personalized Multi-Agent Tutoring Experience</p>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('''
        <p class="hero-description">
        Transform your learning journey with our AI-powered tutoring system. 
        Get personalized lessons, interactive quizzes, and adaptive feedback 
        tailored to your unique learning style and pace.
        </p>
        ''', unsafe_allow_html=True)

    # Feature Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
        <div class="custom-card">
            <h3 style="color: #667eea;">🎯 Personalized Learning</h3>
            <p style="color: #a0a0c0;">Content adapted to your grade level and interests</p>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="custom-card">
            <h3 style="color: #764ba2;">🤖 Multi-Agent Support</h3>
            <p style="color: #a0a0c0;">Various AI agents for different learning styles</p>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="custom-card">
            <h3 style="color: #667eea;">📊 Adaptive Quizzes</h3>
            <p style="color: #a0a0c0;">Track progress with intelligent assessments</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.page = 'screener'
            st.rerun()

# Student Screener Page


def screener_page():
    st.markdown('<h1 style="color: #667eea;">Let\'s Get to Know You</h1>',
                unsafe_allow_html=True)
    st.markdown('<p style="color: #a0a0c0;">Help us personalize your learning experience</p>',
                unsafe_allow_html=True)

    # Chat interface for screener
    chat_container = st.container()

    with chat_container:
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Screener questions
        questions = [
            "What grade are you in? (e.g., Grade 10, University Year 2)",
            "What's your field of interest? (e.g., Science, Mathematics, Literature)",
            "How would you describe your learning pace? (Slow, Moderate, Fast)"
        ]

        if st.session_state.screener_step == 0:
            with st.chat_message("assistant"):
                st.write(
                    "Hello! I'm your AI Learning Companion. Let's start by getting to know you better.")
                st.write(questions[0])

            user_input = st.chat_input("Your answer...")
            if user_input:
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_input})
                st.session_state.student_profile['grade'] = user_input
                st.session_state.screener_step = 1
                st.rerun()

        elif st.session_state.screener_step == 1:
            with st.chat_message("assistant"):
                st.write(questions[1])

            user_input = st.chat_input("Your answer...")
            if user_input:
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_input})
                st.session_state.student_profile['interest'] = user_input
                st.session_state.screener_step = 2
                st.rerun()

        elif st.session_state.screener_step == 2:
            with st.chat_message("assistant"):
                st.write(questions[2])

            user_input = st.chat_input("Your answer...")
            if user_input:
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_input})
                st.session_state.student_profile['pace'] = user_input
                st.session_state.screener_step = 3
                st.rerun()

        elif st.session_state.screener_step == 3:
            with st.chat_message("assistant"):
                st.write(f"Perfect! I've created your personalized profile:")
                st.write(
                    f"- **Grade Level:** {st.session_state.student_profile.get('grade', 'N/A')}")
                st.write(
                    f"- **Interest Area:** {st.session_state.student_profile.get('interest', 'N/A')}")
                st.write(
                    f"- **Learning Pace:** {st.session_state.student_profile.get('pace', 'N/A')}")
                st.write("Let's start learning!")

            if st.button("Continue to Learning", use_container_width=True):
                st.session_state.page = 'learning'
                st.session_state.chat_history = []
                st.rerun()

# Learning Page


def learning_page():
    st.markdown('<h1 style="color: #667eea;">Learning Hub</h1>',
                unsafe_allow_html=True)

    # Display student profile
    if st.session_state.student_profile:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">📚</div>
                <div class="metric-label">{st.session_state.student_profile.get('grade', 'N/A')}</div>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">🎯</div>
                <div class="metric-label">{st.session_state.student_profile.get('interest', 'N/A')}</div>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">⚡</div>
                <div class="metric-label">{st.session_state.student_profile.get('pace', 'N/A')} Pace</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Learning topic input
    col1, col2 = st.columns([3, 1])
    with col1:
        learning_topic = st.text_input(
            "What do you want to learn today?",
            placeholder="e.g., Photosynthesis, Quadratic Equations, World War II...",
            key="topic_input"
        )
    with col2:
        if st.button("Start Learning", use_container_width=True):
            if learning_topic:
                st.session_state.learning_topic = learning_topic

    # File upload section
    st.markdown("### 📁 Upload Study Materials")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'pptx', 'docx'],
        help="Upload PDF, PowerPoint, or Word documents"
    )

    if uploaded_file is not None:
        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    # Learning format options
    st.markdown("### 🎨 Choose Learning Format")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📝 Text", use_container_width=True):
            st.session_state.learning_format = "text"
    with col2:
        if st.button("🖼️ Images", use_container_width=True):
            st.info("Image generation coming soon!")
    with col3:
        if st.button("🧠 Mind Maps", use_container_width=True):
            st.info("Mind map feature coming soon!")
    with col4:
        if st.button("🔊 Audio", use_container_width=True):
            st.info("Audio narration coming soon!")

    # Chat interface for learning
    st.markdown("### 💬 Learning Assistant")

    chat_container = st.container(height=400)
    with chat_container:
        if st.session_state.learning_topic:
            with st.chat_message("assistant"):
                st.write(
                    f"Great! Let's learn about **{st.session_state.learning_topic}**.")
                st.write("Here's a comprehensive overview:")
                st.write(f"""
                Based on your profile ({st.session_state.student_profile.get('grade', 'N/A')} level, 
                {st.session_state.student_profile.get('pace', 'moderate')} pace), 
                I'll explain {st.session_state.learning_topic} in a way that's perfect for you.
                
                **Key Concepts:**
                1. Introduction and basic principles
                2. Core mechanisms and processes
                3. Real-world applications
                4. Common misconceptions
                
                Feel free to ask any questions!
                """)

    user_question = st.chat_input("Ask a question about the topic...")
    if user_question:
        with chat_container:
            with st.chat_message("user"):
                st.write(user_question)
            with st.chat_message("assistant"):
                st.write("That's a great question! Let me explain...")
                with st.spinner("Thinking..."):
                    time.sleep(1)
                st.write(
                    f"Here's a detailed explanation about your question regarding {st.session_state.learning_topic}...")

    # Navigation to quiz
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.learning_topic:
        if st.button("📊 Test Your Knowledge", use_container_width=True):
            st.session_state.page = 'quiz'
            st.rerun()

# Quiz Page


def quiz_page():
    st.markdown('<h1 style="color: #667eea;">Knowledge Assessment</h1>',
                unsafe_allow_html=True)

    if st.session_state.learning_topic:
        st.markdown(
            f'<p style="color: #a0a0c0;">Testing your understanding of: <b>{st.session_state.learning_topic}</b></p>', unsafe_allow_html=True)

    # Sample quiz questions
    if not st.session_state.quiz_questions:
        st.session_state.quiz_questions = [
            {
                "question": f"Which of the following best describes {st.session_state.learning_topic or 'this concept'}?",
                "type": "mcq",
                "options": ["Option A: Basic definition", "Option B: Advanced definition", "Option C: Related concept", "Option D: Incorrect definition"],
                "correct": 0
            },
            {
                "question": f"True or False: {st.session_state.learning_topic or 'This concept'} is important in modern applications.",
                "type": "tf",
                "correct": True
            },
            {
                "question": f"Explain in your own words what {st.session_state.learning_topic or 'this concept'} means.",
                "type": "short",
                "sample": "A comprehensive explanation would include key points and examples."
            }
        ]

    # Quiz form
    with st.form("quiz_form"):
        for i, q in enumerate(st.session_state.quiz_questions):
            st.markdown(f"### Question {i+1}")
            st.write(q["question"])

            if q["type"] == "mcq":
                answer = st.radio(f"q{i}", q["options"], key=f"mcq_{i}")
                st.session_state.quiz_answers[i] = answer

            elif q["type"] == "tf":
                answer = st.radio(f"q{i}", ["True", "False"], key=f"tf_{i}")
                st.session_state.quiz_answers[i] = answer

            elif q["type"] == "short":
                answer = st.text_area(f"Your answer:", key=f"short_{i}")
                st.session_state.quiz_answers[i] = answer

            st.markdown("---")

        submitted = st.form_submit_button(
            "Submit Quiz", use_container_width=True)

        if submitted:
            # Calculate score (simplified)
            correct_answers = 0
            total_questions = len(st.session_state.quiz_questions)

            for i, q in enumerate(st.session_state.quiz_questions):
                if q["type"] == "mcq":
                    if st.session_state.quiz_answers.get(i) == q["options"][q["correct"]]:
                        correct_answers += 1
                elif q["type"] == "tf":
                    user_answer = st.session_state.quiz_answers.get(
                        i) == "True"
                    if user_answer == q["correct"]:
                        correct_answers += 1
                elif q["type"] == "short":
                    # Simplified: give credit if answer is not empty
                    if st.session_state.quiz_answers.get(i, "").strip():
                        correct_answers += 1

            score_percentage = (correct_answers / total_questions) * 100
            st.session_state.quiz_score = score_percentage

            # Display results
            st.markdown("## Quiz Results")

            if score_percentage >= 70:
                st.success(f"🎉 Excellent! You scored {score_percentage:.0f}%")
                st.balloons()
            elif score_percentage >= 50:
                st.warning(
                    f"📚 Good effort! You scored {score_percentage:.0f}%. Keep practicing!")
            else:
                st.error(
                    f"💪 You scored {score_percentage:.0f}%. Let's review the material again.")

            # Progress bar
            st.progress(score_percentage / 100)

            # Feedback for each question
            st.markdown("### Detailed Feedback")
            for i, q in enumerate(st.session_state.quiz_questions):
                with st.expander(f"Question {i+1}"):
                    st.write(q["question"])
                    if q["type"] == "short":
                        st.write(
                            f"**Your answer:** {st.session_state.quiz_answers.get(i, 'No answer')}")
                        st.write(f"**Sample answer:** {q['sample']}")
                    else:
                        st.write(
                            f"**Your answer:** {st.session_state.quiz_answers.get(i, 'No answer')}")

            # Retry option for low scores
            if score_percentage < 70:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📖 Review Material", use_container_width=True):
                        st.session_state.page = 'learning'
                        st.session_state.quiz_questions = []
                        st.session_state.quiz_answers = {}
                        st.rerun()
                with col2:
                    if st.button("🔄 Retake Quiz", use_container_width=True):
                        st.session_state.quiz_answers = {}
                        st.rerun()

# Sidebar navigation


def sidebar_navigation():
    with st.sidebar:
        st.markdown(
            '<h2 style="color: #667eea;text-align: center;">Navigation</h2>', unsafe_allow_html=True)

        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'hero'
            st.rerun()

        if st.button("👤 Student Profile", use_container_width=True):
            st.session_state.page = 'screener'
            st.rerun()

        if st.button("📚 Learning Hub", use_container_width=True):
            st.session_state.page = 'learning'
            st.rerun()

        if st.button("📊 Quiz", use_container_width=True):
            st.session_state.page = 'quiz'
            st.rerun()

        st.markdown("---")

        # Display student profile if available
        if st.session_state.student_profile:
            st.markdown(
                '<h3 style="color: #764ba2;">Your Profile</h3>', unsafe_allow_html=True)
            st.write(
                f"**Grade:** {st.session_state.student_profile.get('grade', 'Not set')}")
            st.write(
                f"**Interest:** {st.session_state.student_profile.get('interest', 'Not set')}")
            st.write(
                f"**Pace:** {st.session_state.student_profile.get('pace', 'Not set')}")

        # Progress metrics
        if st.session_state.quiz_score > 0:
            st.markdown("---")
            st.markdown('<h3 style="color: #764ba2;">Progress</h3>',
                        unsafe_allow_html=True)
            st.metric("Last Quiz Score", f"{st.session_state.quiz_score:.0f}%")

# Main app


def main():
    init_session_state()
    load_css()
    sidebar_navigation()

    # Page routing
    if st.session_state.page == 'hero':
        hero_page()
    elif st.session_state.page == 'screener':
        screener_page()
    elif st.session_state.page == 'learning':
        learning_page()
    elif st.session_state.page == 'quiz':
        quiz_page()


if __name__ == "__main__":
    main()
