# YourTeacher - Personalized Education System

A comprehensive educational system powered by OpenAI Agents SDK that provides personalized learning experiences through intelligent agent coordination.

## 🎯 Overview

YourTeacher consists of three specialized agents that work together to provide personalized education:

1. **Student Screener Agent** - Assesses students based on grade level, field of study, and cognitive abilities
2. **Personalized Teaching Agent** - Delivers customized lessons adapted to individual student profiles
3. **Coordinator Agent** - Manages workflow between agents and tracks learning progress

## 🏗️ Architecture

```
YourTeacher/
├── agents/
│   ├── __init__.py                    # Package initialization
│   ├── screening_agent.py             # Student assessment agent
│   ├── teaching_assistant_agent.py    # Personalized teaching agent
│   ├── coordinator_agent.py           # Workflow coordination agent
│   └── global_agent_config.py         # System configuration
├── main.py                            # Main demonstration
├── example_usage.py                   # Individual agent examples
└── README.md                          # This file
```

## 🚀 Features

### Student Screener Agent

-   Comprehensive student assessment
-   Grade level evaluation
-   Field of study identification
-   Cognitive ability testing
-   Learning style analysis
-   Personalized recommendations

### Personalized Teaching Agent

-   Adaptive teaching methods
-   Multi-modal learning support (visual, auditory, kinesthetic)
-   Subject-specific adaptations
-   Real-time difficulty adjustment
-   Progress-based feedback
-   Interactive learning elements

### Coordinator Agent

-   Workflow orchestration
-   Progress tracking
-   Learning path optimization
-   Multi-agent coordination
-   Performance analytics
-   Intervention recommendations

## 📋 Requirements

-   Python 3.12+
-   OpenAI Agents SDK 0.3.1+
-   Streamlit 1.49.1+

## 🔧 Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd YourTeacher
```

2. Install dependencies:

```bash
pip install -r requirements.txt
# or if using uv:
uv sync
```

3. Set up your OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## 💡 Usage

### Quick Start

Run the main demonstration:

```bash
python main.py
```

### Individual Agent Examples

Run specific agent examples:

```bash
python example_usage.py
```

### Using in Your Code

```python
from agents import educational_system, Runner

# Get agents
screener = educational_system.get_screening_agent()
teacher = educational_system.get_teaching_agent()
coordinator = educational_system.get_coordinator_agent()

# Screen a student
student_info = {"name": "John", "grade": "10th", "interests": ["Math"]}
agent, prompt = screener.screen_student(student_info)
result = Runner.run_sync(agent, prompt)

# Teach based on profile
student_profile = {"grade": "10th", "field": "STEM", "cognitive_ability": "High"}
agent, prompt = teacher.teach_student(student_profile, "Mathematics", "Algebra")
result = Runner.run_sync(agent, prompt)
```

## 🎓 Educational Workflow

1. **Student Onboarding**

    - Initial information collection
    - Comprehensive screening assessment
    - Profile generation

2. **Personalized Teaching**

    - Adaptive lesson delivery
    - Real-time difficulty adjustment
    - Multi-modal content presentation

3. **Progress Monitoring**

    - Continuous assessment
    - Learning analytics
    - Intervention recommendations

4. **Optimization**
    - Teaching method refinement
    - Learning path adjustment
    - Performance improvement

## 🔧 Configuration

The system uses Gemini API through OpenAI-compatible interface. Update the configuration in `main.py`:

```python
gemini_api_key = "your_api_key_here"
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

## 📊 Agent Capabilities

### Student Assessment

-   Academic performance evaluation
-   Learning style identification
-   Cognitive ability testing
-   Strength and weakness analysis
-   Personalized recommendations

### Teaching Adaptation

-   Grade-appropriate content
-   Field-specific examples
-   Cognitive load management
-   Learning style accommodation
-   Progress-based pacing

### System Coordination

-   Multi-agent orchestration
-   Learning path optimization
-   Progress tracking
-   Performance analytics
-   Intervention planning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions, issues, or contributions, please open an issue on GitHub or contact the development team.

---

**YourTeacher** - Empowering personalized education through intelligent agent coordination.
