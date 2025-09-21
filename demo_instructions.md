# 🎓 YourTeacher Streamlit App - Demo Instructions

## 🚀 How to Run the App

### Option 1: Quick Start (Recommended)

```bash
cd /Users/hamzaadil/Documents/Coding/YourTeacher
python run_app.py
```

### Option 2: Direct Streamlit

```bash
cd /Users/hamzaadil/Documents/Coding/YourTeacher
streamlit run streamlit_app.py
```

## 🎯 What You'll Experience

### 1. **Landing Page**

When the app loads, you'll see:

```
🎓 YourTeacher - AI Learning System
=====================================

📊 System Status (Sidebar)
🤖 Current Agent: Student Screener Agent
💬 Conversation History: (Empty, ready to start)
```

### 2. **Assessment Phase** 🔍

The Screener Agent will appear with a **pink gradient card**:

```
🔍 Student Screener Agent
Phase: Assessment Phase
Assessing your learning profile and cognitive abilities
```

**Sample Interaction:**

-   **Agent**: "Hello! Welcome to YourTeacher! What's your name?"
-   **You**: "My name is Alex"
-   **Agent**: "Nice to meet you Alex! How old are you?"
-   **You**: "I'm 16 years old"

**Visual Features:**

-   🔧 Tool usage notifications when agent processes your responses
-   ✅ Tool results showing cognitive assessment scores
-   📊 Progress tracker updating in real-time

### 3. **Agent Handoff** 🔄

When assessment is complete:

```
🔄 Agent Handoff: Student Screener Agent → Teaching Agent
```

**Teaching Agent appears with blue gradient card:**

```
👨‍🏫 Teaching Agent
Phase: Learning Phase
Providing personalized lessons based on your profile
```

### 4. **Learning Phase** 👨‍🏫

**Sample Teaching Interaction:**

-   **Agent**: "Hi Alex! Based on your profile, you're a visual learner with high cognitive ability. What would you like to learn about?"
-   **You**: "I want to learn about photosynthesis"
-   **Agent**: Uses tools to set topic and generate personalized content
-   **Visual**: 🔧 Tool notifications, ✅ Content generation confirmations

### 5. **Quiz Handoff** 📝

After teaching:

```
🔄 Agent Handoff: Teaching Agent → Quiz Agent
```

**Quiz Agent with green gradient card:**

```
📝 Quiz Agent
Phase: Validation Phase
Testing your understanding with customized quizzes
```

### 6. **Assessment Results** 📊

**Real-time progress tracking shows:**

-   ✅ Assessment Complete: Alex, High cognitive ability, Visual learner
-   ✅ Concept Taught: Biology - Photosynthesis
-   ✅ Quiz Passed: 4/5 (80%)

## 🎨 Visual Experience

### **Sidebar Features**

```
📊 System Status
├── ✅ Assessment Complete
│   👤 Student: Alex
│   🧠 Cognitive Level: High
│   🎯 Learning Style: Visual
├── ✅ Concept Taught
│   📚 Subject: Biology
│   📖 Topic: Photosynthesis
└── ✅ Quiz Passed: 4/5

🤖 Current Agent
[Beautiful gradient card showing active agent]

⚙️ Controls
[🔄 Reset Session button]

👤 Student Profile
[JSON display of complete profile]
```

### **Main Content**

```
💬 Conversation History
[Beautifully formatted chat messages with:]
- 👤 User messages in blue boxes
- 🤖 Agent messages in green boxes
- 🔄 Handoff notifications in pink
- 🔧 Tool usage in gray boxes
- ✅ Tool results highlighted

💭 Your Response
[Text area with Send Message button]
[❓ Get Help button for context-aware assistance]
```

### **Right Panel**

```
🔄 Learning Workflow
├── ✅ Screener (Completed)
├── ✅ Teacher (Completed)
└── ✅ Quiz (Completed)

📈 Session Stats
├── 💬 Messages: 15
├── 🔧 Tool Calls: 8
└── 🔄 Handoffs: 2

💡 Tips
├── 💡 Be honest during assessment
├── 💡 Ask for clarification
├── 💡 Take your time with quiz
└── 💡 Learn multiple topics
```

## 🎮 Interactive Features

### **Smart Input System**

-   **Context-aware help**: Help button provides agent-specific guidance
-   **Auto-clear**: Input clears after sending
-   **Validation**: Prevents empty messages

### **Real-time Updates**

-   **Instant feedback**: See agent processing in real-time
-   **Progress tracking**: Visual indicators update automatically
-   **Session persistence**: State maintained throughout interaction

### **Error Handling**

-   **Graceful failures**: User-friendly error messages
-   **Recovery options**: Continue conversation after errors
-   **Reset capability**: Fresh start anytime

## 🌟 Special Features

### **Agent Personality**

Each agent has distinct visual identity:

-   **🔍 Screener**: Pink gradient, assessment focus
-   **👨‍🏫 Teacher**: Blue gradient, educational focus
-   **📝 Quiz**: Green gradient, validation focus

### **Tool Transparency**

Users see exactly what's happening:

-   **🔧 Tool Call**: "Agent is using a tool..."
-   **✅ Tool Result**: "Assessment completed. Score: 8/10"
-   **Real-time processing**: No black box experience

### **Adaptive Interface**

-   **Mobile responsive**: Works on all devices
-   **Progressive disclosure**: Information revealed as needed
-   **Context-sensitive**: Help and tips change based on current phase

## 🎯 Expected User Journey

1. **Welcome** → Clear system introduction
2. **Assessment** → Friendly cognitive evaluation
3. **Profile Creation** → Transparent capability assessment
4. **Topic Selection** → Student-driven learning choice
5. **Personalized Teaching** → Adapted content delivery
6. **Knowledge Validation** → Custom quiz experience
7. **Results & Next Steps** → Achievement recognition

## 💡 Pro Tips for Demo

-   **Show the handoffs**: Highlight how agents seamlessly transfer control
-   **Demonstrate personalization**: Show how responses adapt to student profile
-   **Highlight tool usage**: Point out the transparency of AI operations
-   **Use the progress tracker**: Show real-time learning journey visualization
-   **Try the help system**: Demonstrate context-aware assistance
-   **Reset and restart**: Show how easy it is to begin fresh sessions

---

**🎓 Ready to experience the future of personalized AI education!**
