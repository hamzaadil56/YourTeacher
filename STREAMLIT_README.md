# 🎓 YourTeacher - Streamlit Frontend

A beautiful and intuitive web interface for the YourTeacher AI Learning System, built with Streamlit.

## 🌟 Features

### 🎨 **Beautiful User Interface**

-   **Gradient-styled agent cards** with unique colors for each agent
-   **Real-time conversation display** with message history
-   **Progress tracking** showing learning journey stages
-   **Responsive design** that works on desktop and mobile

### 🤖 **Agent Workflow Visualization**

-   **Current agent indicator** showing which AI is active
-   **Handoff notifications** when agents transfer control
-   **Tool usage tracking** showing when agents use their capabilities
-   **Phase progression** (Assessment → Learning → Validation)

### 📊 **Interactive Dashboard**

-   **Live progress tracker** showing completion status
-   **Student profile display** once assessment is complete
-   **Session statistics** (messages, tool calls, handoffs)
-   **Learning workflow diagram** showing current step

### 💬 **Enhanced Chat Experience**

-   **Message threading** with timestamps
-   **Agent identification** with unique icons and colors
-   **Tool activity notifications** showing AI working behind the scenes
-   **Input validation** and error handling

## 🚀 Quick Start

### Method 1: Using the Run Script (Recommended)

```bash
python run_app.py
```

### Method 2: Direct Streamlit Command

```bash
streamlit run streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎯 How It Works

### 1. **Assessment Phase** 🔍

-   **Screener Agent** conducts comprehensive evaluation
-   Collects basic information (name, age, grade)
-   Performs cognitive ability tests
-   Identifies learning preferences
-   **Visual Feedback**: Pink gradient card, progress indicators

### 2. **Learning Phase** 👨‍🏫

-   **Teaching Agent** provides personalized lessons
-   Adapts content based on student profile
-   Uses appropriate teaching methods
-   **Visual Feedback**: Blue gradient card, topic tracking

### 3. **Validation Phase** 📝

-   **Quiz Agent** creates customized assessments
-   Evaluates understanding in real-time
-   Provides detailed feedback and scores
-   **Visual Feedback**: Green gradient card, score display

## 🎨 UI Components

### **Sidebar Features**

-   **📊 System Status**: Real-time progress tracking
-   **🤖 Current Agent**: Active agent information
-   **⚙️ Controls**: Session reset and management
-   **👤 Student Profile**: Complete profile once assessed

### **Main Content Area**

-   **💬 Conversation History**: Full chat with beautiful formatting
-   **💭 Input Area**: Message composition with help system
-   **📈 Session Stats**: Live metrics and statistics
-   **💡 Tips**: Contextual guidance for users

### **Visual Elements**

-   **Agent Cards**: Color-coded with gradients
    -   🔍 Screener: Pink gradient (`#f093fb → #f5576c`)
    -   👨‍🏫 Teacher: Blue gradient (`#4facfe → #00f2fe`)
    -   📝 Quiz: Green gradient (`#43e97b → #38f9d7`)
-   **Message Bubbles**: Distinct styling for user vs agent messages
-   **Tool Notifications**: Highlighted activity indicators
-   **Handoff Alerts**: Special notifications for agent transitions

## 🔧 Technical Details

### **State Management**

-   **Session persistence** using Streamlit's session state
-   **Context preservation** across agent handoffs
-   **Conversation history** with full message threading
-   **Error recovery** with graceful fallbacks

### **Agent Integration**

-   **Async processing** for smooth user experience
-   **Real-time updates** with automatic page refresh
-   **Tool call visualization** showing AI activity
-   **Error handling** with user-friendly messages

### **Performance Features**

-   **Efficient rendering** with selective updates
-   **Memory management** for long conversations
-   **Responsive design** adapting to screen size
-   **Fast load times** with optimized components

## 🎮 User Experience Flow

### **First-Time User Journey**

1. **Welcome Screen**: Clear introduction and system overview
2. **Assessment Start**: Friendly screener agent introduction
3. **Profile Building**: Interactive cognitive assessment
4. **Learning Selection**: Choose topics based on interests
5. **Personalized Teaching**: Adapted content delivery
6. **Knowledge Validation**: Customized quiz experience
7. **Progress Celebration**: Achievement recognition

### **Returning User Features**

-   **Session continuity** if browser supports it
-   **Profile reuse** for faster setup
-   **Learning history** tracking (future enhancement)
-   **Preference memory** for improved experience

## 🛠️ Customization Options

### **Styling**

-   Modify CSS in the `st.markdown()` sections
-   Change gradient colors in agent card styles
-   Adjust layout proportions in column definitions
-   Update icons and emojis throughout

### **Functionality**

-   Add new agent types by extending the agent info dictionary
-   Implement additional progress tracking metrics
-   Create custom input validation rules
-   Add export features for conversation history

## 🔍 Troubleshooting

### **Common Issues**

-   **Port conflicts**: Change port in `run_app.py` if 8501 is busy
-   **Import errors**: Ensure all dependencies are installed
-   **Agent errors**: Check terminal output for detailed error messages
-   **Browser issues**: Try refreshing or clearing cache

### **Performance Tips**

-   **Reset session** if conversation becomes too long
-   **Use Chrome or Firefox** for best compatibility
-   **Close other tabs** if experiencing slowdowns
-   **Check network connection** for API calls

## 📱 Mobile Compatibility

The interface is fully responsive and works great on:

-   **📱 Smartphones**: Optimized touch interface
-   **📟 Tablets**: Perfect for educational use
-   **💻 Laptops**: Full feature experience
-   **🖥️ Desktops**: Maximum screen real estate

## 🎯 Future Enhancements

-   **📊 Learning Analytics Dashboard**
-   **🔊 Voice Input/Output Support**
-   **📁 Session Save/Load Functionality**
-   **👥 Multi-User Support**
-   **🎨 Theme Customization**
-   **📈 Progress Visualization Charts**

---

**🎓 YourTeacher Streamlit App** - Making AI education accessible, beautiful, and effective!
