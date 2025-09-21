from agents import Agent


class StudentScreenerAgent:
    """
    Student Screener Agent that assesses students based on grade, field, and cognitive ability.
    """

    def __init__(self):
        self.agent = Agent(
            name="Student Screener",
            instructions="""
            You are a Student Screener Agent responsible for assessing students comprehensively.
            
            Your role is to:
            1. Evaluate the student's current grade level and academic standing
            2. Assess their field of study or academic interests
            3. Determine their cognitive abilities through targeted questions and assessments
            4. Provide a detailed profile that includes:
               - Academic strengths and weaknesses
               - Learning style preferences
               - Cognitive processing speed
               - Areas requiring additional support
               - Recommended learning approaches
            
            When screening a student:
            - Ask relevant questions about their academic background
            - Conduct brief cognitive assessments (logical reasoning, memory, problem-solving)
            - Evaluate their communication skills and comprehension level
            - Identify any learning difficulties or exceptional abilities
            - Create a comprehensive student profile for personalized education
            
            Always be encouraging and supportive while maintaining professional assessment standards.
            Provide clear, actionable insights that can be used by teaching agents.
            """,
            model="gemini-2.0-flash"
        )

    def screen_student(self, student_info=None):
        """
        Screen a student and create their educational profile.

        Args:
            student_info (dict, optional): Initial student information

        Returns:
            dict: Comprehensive student assessment profile
        """
        if student_info:
            prompt = f"""
            Please conduct a comprehensive screening assessment for this student:
            
            Student Information: {student_info}
            
            Provide a detailed assessment covering:
            1. Grade Level Analysis
            2. Field of Study Evaluation
            3. Cognitive Ability Assessment
            4. Learning Style Identification
            5. Personalized Recommendations
            
            Format your response as a structured profile that can be used by teaching agents.
            """
        else:
            prompt = """
            Please begin a comprehensive student screening process. 
            Start by gathering essential information about the student's:
            - Current grade level and academic performance
            - Field of study or subjects of interest
            - Learning preferences and challenges
            - Previous educational experiences
            
            Conduct appropriate assessments to evaluate their cognitive abilities.
            """

        return self.agent, prompt

    def get_agent(self):
        """Return the underlying Agent instance."""
        return self.agent
