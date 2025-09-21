import streamlit as st
import asyncio
import uuid
from typing import Dict, Any, List
import time
from datetime import datetime

# Import your educational system
from main import (
    StudentLearningContext,
    screener_agent,
    teaching_agent,
    quiz_agent,
    Runner,
    MessageOutputItem,
    HandoffOutputItem,
    ToolCallItem,
    ToolCallOutputItem,
    ItemHelpers
)

# Page configuration
st.set_page_config(
    page_title="YourTeacher - AI Learning System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Hide Streamlit's default code block styling for div elements */
    .stMarkdown div[data-testid="stMarkdownContainer"] pre {
        display: none !important;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Dark mode support for main header */
    [data-theme="dark"] .main-header {
        color: #4fc3f7;
    }
    
    /* Agent card base styling */
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white !important;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Specific agent card colors */
    .screener-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
    }
    
    .teaching-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white !important;
    }
    
    .quiz-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white !important;
    }
    
    /* Tool usage styling with dark mode support */
    .tool-usage {
        background-color: #f0f2f6;
        color: #1f2937 !important;
        padding: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    /* Dark mode tool usage */
    [data-theme="dark"] .tool-usage {
        background-color: #374151;
        color: #f9fafb !important;
        border-left-color: #60a5fa;
    }
    
    /* Handoff notification */
    .handoff-notification {
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
        color: #1f2937 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat message base styling */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* User message styling */
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #1565c0 !important;
    }
    
    /* Dark mode user message */
    [data-theme="dark"] .user-message {
        background-color: #1e3a8a;
        color: #bfdbfe !important;
        border-left-color: #60a5fa;
    }
    
    /* Agent message styling */
    .agent-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
        color: #2e7d32 !important;
    }
    
    /* Dark mode agent message */
    [data-theme="dark"] .agent-message {
        background-color: #14532d;
        color: #bbf7d0 !important;
        border-left-color: #4ade80;
    }
    
    /* Progress container */
    .progress-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #1f2937 !important;
    }
    
    /* Dark mode progress container */
    [data-theme="dark"] .progress-container {
        background-color: #374151;
        color: #f9fafb !important;
    }
    
    /* Ensure all text in custom divs is visible in dark mode */
    [data-theme="dark"] .agent-card h3,
    [data-theme="dark"] .agent-card p,
    [data-theme="dark"] .handoff-notification {
        color: white !important;
    }
    
    /* Fix for any remaining text visibility issues */
    .chat-message strong {
        font-weight: bold !important;
    }
    
    [data-theme="dark"] .user-message strong {
        color: #bfdbfe !important;
    }
    
    [data-theme="dark"] .agent-message strong {
        color: #bbf7d0 !important;
    }
    
    /* Hide any unwanted code blocks that might appear */
    .stMarkdown pre {
        display: none !important;
    }
    
    .stMarkdown code {
        background: transparent !important;
        padding: 0 !important;
        font-family: inherit !important;
    }
    
    /* Additional code block hiding */
    div[data-testid="stMarkdownContainer"] pre,
    div[data-testid="stMarkdownContainer"] code[class*="language-"] {
        display: none !important;
    }
    
    /* Prevent code highlighting */
    .stMarkdown .highlight {
        background: transparent !important;
    }
    
    /* Force text to be visible in all themes */
    .chat-message, 
    .tool-usage, 
    .handoff-notification,
    .agent-card {
        font-size: 14px !important;
        line-height: 1.5 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state


def init_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = screener_agent
    if 'context' not in st.session_state:
        st.session_state.context = StudentLearningContext()
    if 'input_items' not in st.session_state:
        st.session_state.input_items = [{
            "content": "Hello! I'm ready to start my personalized learning journey.",
            "role": "user"
        }]
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = uuid.uuid4().hex[:16]
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False


def get_agent_info(agent):
    """Get agent information for display"""
    agent_info = {
        "Student Screener Agent": {
            "icon": "🔍",
            "color": "screener-card",
            "description": "Assessing your learning profile and cognitive abilities",
            "phase": "Assessment Phase"
        },
        "Teaching Agent": {
            "icon": "👨‍🏫",
            "color": "teaching-card",
            "description": "Providing personalized lessons based on your profile",
            "phase": "Learning Phase"
        },
        "Quiz Agent": {
            "icon": "📝",
            "color": "quiz-card",
            "description": "Testing your understanding with customized quizzes",
            "phase": "Validation Phase"
        }
    }
    return agent_info.get(agent.name, {
        "icon": "🤖",
        "color": "agent-card",
        "description": "AI Assistant",
        "phase": "Active"
    })


def display_progress_tracker():
    """Display the learning progress tracker"""
    context = st.session_state.context

    col1, col2, col3 = st.columns(3)

    with col1:
        if context.screening_complete:
            st.success("✅ **Assessment Complete**")
            if context.student_name:
                st.write(f"👤 **Student:** {context.student_name}")
            if context.cognitive_ability:
                st.write(f"🧠 **Cognitive Level:** {context.cognitive_ability}")
            if context.learning_style:
                st.write(f"🎯 **Learning Style:** {context.learning_style}")
        else:
            st.info("🔍 **Assessment In Progress**")

    with col2:
        if context.concept_taught and context.current_topic:
            st.success("✅ **Concept Taught**")
            st.write(f"📚 **Subject:** {context.current_subject}")
            st.write(f"📖 **Topic:** {context.current_topic}")
        elif context.screening_complete:
            st.info("👨‍🏫 **Ready for Learning**")
        else:
            st.warning("⏳ **Waiting for Assessment**")

    with col3:
        if context.quiz_score is not None and context.quiz_total is not None:
            score_pct = (context.quiz_score / context.quiz_total) * 100
            if score_pct >= 80:
                st.success(
                    f"✅ **Quiz Passed: {context.quiz_score}/{context.quiz_total}**")
            else:
                st.warning(
                    f"📝 **Quiz Score: {context.quiz_score}/{context.quiz_total}**")
        elif context.concept_taught:
            st.info("📝 **Ready for Quiz**")
        else:
            st.warning("⏳ **Waiting for Teaching**")


async def process_agent_interaction(user_input):
    """Process interaction with the current agent"""
    try:
        # Add user input to conversation
        if user_input:
            st.session_state.input_items.append({
                "content": user_input,
                "role": "user"
            })

            # Add to conversation history
            st.session_state.conversation_history.append({
                "type": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })

        # Run the agent
        result = await Runner.run(
            st.session_state.current_agent,
            st.session_state.input_items,
            context=st.session_state.context
        )

        # Process results
        for new_item in result.new_items:
            agent_info = get_agent_info(new_item.agent)

            if isinstance(new_item, MessageOutputItem):
                message = ItemHelpers.text_message_output(new_item)
                st.session_state.conversation_history.append({
                    "type": "agent",
                    "agent_name": new_item.agent.name,
                    "content": message,
                    "timestamp": datetime.now(),
                    "icon": agent_info["icon"]
                })

            elif isinstance(new_item, HandoffOutputItem):
                st.session_state.conversation_history.append({
                    "type": "handoff",
                    "source": new_item.source_agent.name,
                    "target": new_item.target_agent.name,
                    "timestamp": datetime.now()
                })

            elif isinstance(new_item, ToolCallItem):
                st.session_state.conversation_history.append({
                    "type": "tool_call",
                    "agent_name": new_item.agent.name,
                    "timestamp": datetime.now(),
                    "icon": agent_info["icon"]
                })

            elif isinstance(new_item, ToolCallOutputItem):
                st.session_state.conversation_history.append({
                    "type": "tool_result",
                    "content": new_item.output,
                    "timestamp": datetime.now()
                })

        # Update for next iteration
        st.session_state.input_items = result.to_input_list()
        st.session_state.current_agent = result.last_agent

        return True

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        return False


def display_conversation_history():
    """Display the conversation history with beautiful formatting"""
    st.subheader("💬 Conversation History")

    if not st.session_state.conversation_history:
        st.info("👋 Start your conversation by typing a message below!")
        return

    for i, item in enumerate(st.session_state.conversation_history):
        if item["type"] == "user":
            # Clean the content to prevent HTML rendering issues
            clean_content = str(item["content"]).replace(
                "<", "&lt;").replace(">", "&gt;")
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {clean_content}
            </div>
            """, unsafe_allow_html=True)

        elif item["type"] == "agent":
            icon = item.get("icon", "🤖")
            # Clean the content and prevent code block rendering
            clean_content = str(item["content"]).replace(
                "<", "&lt;").replace(">", "&gt;")
            # Remove any potential code block markers
            clean_content = clean_content.replace("```", "")

            st.markdown(f"""
            <div class="chat-message agent-message">
                <strong>{icon} {item["agent_name"]}:</strong><br>
                {clean_content}
            </div>
            """, unsafe_allow_html=True)

        elif item["type"] == "handoff":
            st.markdown(f"""
            <div class="handoff-notification">
                🔄 Agent Handoff: {item["source"]} → {item["target"]}
            </div>
            """, unsafe_allow_html=True)

        elif item["type"] == "tool_call":
            icon = item.get("icon", "🤖")
            st.markdown(f"""
            <div class="tool-usage">
                🔧 <strong>{icon} {item["agent_name"]}</strong> is using a tool...
            </div>
            """, unsafe_allow_html=True)

        elif item["type"] == "tool_result":
            # Clean tool result content
            clean_content = str(item["content"]).replace(
                "<", "&lt;").replace(">", "&gt;")
            st.markdown(f"""
            <div class="tool-usage">
                ✅ <strong>Tool Result:</strong> {clean_content}
            </div>
            """, unsafe_allow_html=True)


def display_current_agent_info():
    """Display information about the current active agent"""
    agent_info = get_agent_info(st.session_state.current_agent)

    st.markdown(f"""
    <div class="agent-card {agent_info['color']}">
        <h3>{agent_info['icon']} {st.session_state.current_agent.name}</h3>
        <p><strong>Phase:</strong> {agent_info['phase']}</p>
        <p>{agent_info['description']}</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    # Initialize session state
    init_session_state()

    # Main header
    st.markdown('<h1 class="main-header">🎓 YourTeacher - AI Learning System</h1>',
                unsafe_allow_html=True)

    # Sidebar with system information
    with st.sidebar:
        st.header("📊 System Status")

        # Progress tracker
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        display_progress_tracker()
        st.markdown('</div>', unsafe_allow_html=True)

        # Current agent info
        st.header("🤖 Current Agent")
        display_current_agent_info()

        # System controls
        st.header("⚙️ Controls")
        if st.button("🔄 Reset Session", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # Student profile (if available)
        if st.session_state.context.screening_complete:
            st.header("👤 Student Profile")
            profile = st.session_state.context.student_profile
            if profile:
                st.json(profile)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Conversation area
        display_conversation_history()

        # Input area
        st.subheader("💭 Your Response")

        # Create input form
        with st.form(key="user_input_form", clear_on_submit=True):
            user_input = st.text_area(
                f"Type your message to {st.session_state.current_agent.name}:",
                height=100,
                placeholder="Type your message here..."
            )

            col_send, col_help = st.columns([1, 1])
            with col_send:
                submit_button = st.form_submit_button(
                    "📤 Send Message", type="primary")
            with col_help:
                if st.form_submit_button("❓ Get Help"):
                    help_message = f"You're currently talking to the {st.session_state.current_agent.name}. "
                    if st.session_state.current_agent.name == "Student Screener Agent":
                        help_message += "This agent will assess your learning profile. Answer questions about yourself honestly."
                    elif st.session_state.current_agent.name == "Teaching Agent":
                        help_message += "This agent will teach you concepts. Tell it what you want to learn about."
                    else:
                        help_message += "This agent will quiz you. Answer the questions to test your understanding."

                    st.info(help_message)

        # Process input
        if submit_button and user_input.strip():
            with st.spinner("🤖 Agent is processing..."):
                success = asyncio.run(
                    process_agent_interaction(user_input.strip()))
                if success:
                    st.rerun()

    with col2:
        # Agent workflow diagram
        st.subheader("🔄 Learning Workflow")

        # Visual workflow
        agents = [
            ("🔍 Screener", st.session_state.context.screening_complete),
            ("👨‍🏫 Teacher", st.session_state.context.concept_taught),
            ("📝 Quiz", st.session_state.context.quiz_score is not None)
        ]

        for i, (agent_name, completed) in enumerate(agents):
            if completed:
                st.success(f"✅ {agent_name}")
            elif i == 0 or agents[i-1][1]:  # Current or next step
                if st.session_state.current_agent.name.startswith(agent_name.split()[1]):
                    st.info(f"🔄 {agent_name} (Active)")
                else:
                    st.info(f"⏳ {agent_name} (Ready)")
            else:
                st.warning(f"⏸️ {agent_name} (Waiting)")

        # Quick stats
        st.subheader("📈 Session Stats")
        stats_container = st.container()
        with stats_container:
            total_messages = len(
                [h for h in st.session_state.conversation_history if h["type"] in ["user", "agent"]])
            tool_calls = len(
                [h for h in st.session_state.conversation_history if h["type"] == "tool_call"])
            handoffs = len(
                [h for h in st.session_state.conversation_history if h["type"] == "handoff"])

            st.metric("💬 Messages", total_messages)
            st.metric("🔧 Tool Calls", tool_calls)
            st.metric("🔄 Handoffs", handoffs)

        # Tips section
        st.subheader("💡 Tips")
        tips = [
            "Be honest during assessment for better personalization",
            "Ask for clarification if you don't understand",
            "Take your time with quiz questions",
            "You can learn multiple topics in one session"
        ]

        for tip in tips:
            st.info(f"💡 {tip}")


if __name__ == "__main__":
    main()
