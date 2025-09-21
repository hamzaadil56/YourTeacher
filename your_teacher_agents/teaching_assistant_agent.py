from agents import Agent


class PersonalizedTeachingAgent:
    """
    Personalized Teaching Assistant Agent that adapts teaching methods based on student profile.
    """

    def __init__(self):
        self.agent = Agent(
            name="Personalized Teaching Assistant",
            instructions="""
            You are a Personalized Teaching Assistant Agent designed to provide customized education.
            
            Your role is to:
            1. Analyze student profiles from the screening agent
            2. Adapt teaching methods to match the student's:
               - Grade level and academic capabilities
               - Field of study and interests
               - Cognitive abilities and learning style
               - Identified strengths and weaknesses
            
            Teaching Strategies:
            - For visual learners: Use diagrams, charts, and visual aids
            - For auditory learners: Provide verbal explanations and discussions
            - For kinesthetic learners: Include hands-on activities and examples
            - For high cognitive ability: Provide advanced concepts and challenges
            - For lower cognitive ability: Break down concepts into smaller steps
            - For different grade levels: Adjust vocabulary and complexity appropriately
            
            Subject-Specific Adaptations:
            - Mathematics: Use appropriate problem-solving techniques and examples
            - Science: Incorporate experiments, real-world applications
            - Literature: Adapt reading levels and discussion complexity
            - History: Use storytelling and timeline approaches
            - Languages: Focus on communication and practical usage
            
            Always:
            - Be patient and encouraging
            - Provide multiple explanation methods
            - Check for understanding regularly
            - Offer additional practice when needed
            - Celebrate progress and achievements
            - Adapt in real-time based on student responses
            """,
            model="gemini-2.0-flash"
        )

    def teach_student(self, student_profile, subject, topic, learning_objectives=None):
        """
        Provide personalized teaching based on student profile.

        Args:
            student_profile (dict): Student assessment from screening agent
            subject (str): Subject to teach
            topic (str): Specific topic within the subject
            learning_objectives (list, optional): Specific learning goals

        Returns:
            tuple: (agent, prompt) for teaching session
        """
        objectives_text = ""
        if learning_objectives:
            objectives_text = f"\nLearning Objectives: {', '.join(learning_objectives)}"

        prompt = f"""
        Please provide personalized teaching for this student:
        
        Student Profile: {student_profile}
        Subject: {subject}
        Topic: {topic}{objectives_text}
        
        Based on the student's profile, please:
        1. Adapt your teaching style to match their learning preferences
        2. Adjust the complexity level appropriate for their grade and cognitive ability
        3. Use examples and explanations relevant to their field of interest
        4. Provide interactive elements suitable for their learning style
        5. Include assessment questions to check understanding
        6. Offer additional resources or practice if needed
        
        Make the lesson engaging, clear, and perfectly tailored to this student's needs.
        """

        return self.agent, prompt

    def provide_feedback(self, student_profile, student_work, subject):
        """
        Provide personalized feedback on student work.

        Args:
            student_profile (dict): Student assessment profile
            student_work (str): Student's submitted work or responses
            subject (str): Subject area

        Returns:
            tuple: (agent, prompt) for feedback session
        """
        prompt = f"""
        Please provide personalized feedback for this student's work:
        
        Student Profile: {student_profile}
        Subject: {subject}
        Student Work: {student_work}
        
        Based on the student's profile and learning needs:
        1. Highlight what they did well (positive reinforcement)
        2. Identify areas for improvement in a supportive manner
        3. Provide specific, actionable suggestions
        4. Adapt feedback style to their cognitive level and learning preferences
        5. Suggest next steps or additional practice if needed
        6. Encourage continued learning and growth
        
        Make your feedback constructive, encouraging, and tailored to help this specific student improve.
        """

        return self.agent, prompt

    def get_agent(self):
        """Return the underlying Agent instance."""
        return self.agent
