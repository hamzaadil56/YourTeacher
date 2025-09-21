from agents import Agent


class CoordinatorAgent:
    """
    Coordinator Agent that manages the workflow between screening and teaching agents.
    """

    def __init__(self):
        self.agent = Agent(
            name="Education Coordinator",
            instructions="""
            You are an Education Coordinator Agent responsible for orchestrating the educational process.
            
            Your role is to:
            1. Manage the workflow between different educational agents
            2. Coordinate student screening and teaching processes
            3. Track student progress and learning outcomes
            4. Make decisions about when to re-assess students
            5. Recommend appropriate teaching strategies and interventions
            6. Ensure continuity in the educational experience
            
            Workflow Management:
            - Initiate student screening when new students join
            - Route students to appropriate teaching agents based on profiles
            - Monitor learning progress and adjust teaching approaches
            - Coordinate between multiple subjects and learning sessions
            - Schedule re-assessments when needed
            - Manage transitions between different learning phases
            
            Decision Making:
            - Determine when a student needs additional screening
            - Identify when teaching methods should be adjusted
            - Recommend specialized interventions or support
            - Coordinate multi-agent teaching for complex topics
            - Manage learning path progression
            
            Progress Tracking:
            - Monitor student engagement and performance
            - Track learning objective completion
            - Identify patterns in student learning
            - Recommend curriculum adjustments
            - Coordinate with parents/guardians when appropriate
            
            Always maintain a holistic view of the student's educational journey and ensure
            all agents work together effectively to provide the best learning experience.
            """,
            model="gemini-2.0-flash"
        )

    def coordinate_new_student(self, student_info=None):
        """
        Coordinate the onboarding process for a new student.

        Args:
            student_info (dict, optional): Initial student information

        Returns:
            tuple: (agent, prompt) for coordination
        """
        prompt = f"""
        A new student needs to be onboarded into our educational system.
        
        Initial Student Information: {student_info if student_info else 'No initial information provided'}
        
        Please coordinate the following process:
        1. Determine what screening assessments are needed
        2. Plan the sequence of educational activities
        3. Identify any special considerations or requirements
        4. Set up the initial learning pathway
        5. Establish success metrics and progress tracking
        
        Provide a comprehensive onboarding plan that ensures this student receives
        the most effective personalized education possible.
        """

        return self.agent, prompt

    def coordinate_learning_session(self, student_profile, learning_request):
        """
        Coordinate a learning session based on student needs.

        Args:
            student_profile (dict): Complete student profile
            learning_request (dict): Specific learning request (subject, topic, etc.)

        Returns:
            tuple: (agent, prompt) for session coordination
        """
        prompt = f"""
        Please coordinate a learning session for this student:
        
        Student Profile: {student_profile}
        Learning Request: {learning_request}
        
        Based on the student's profile and current request:
        1. Determine the most appropriate teaching approach
        2. Identify any prerequisites or preparation needed
        3. Plan the session structure and activities
        4. Set learning objectives and success criteria
        5. Prepare for assessment and feedback collection
        6. Plan follow-up activities or next steps
        
        Ensure the session is optimally designed for this student's learning needs.
        """

        return self.agent, prompt

    def assess_progress(self, student_profile, learning_history, current_performance):
        """
        Assess student progress and recommend next steps.

        Args:
            student_profile (dict): Student profile
            learning_history (list): History of learning sessions and outcomes
            current_performance (dict): Recent performance data

        Returns:
            tuple: (agent, prompt) for progress assessment
        """
        prompt = f"""
        Please assess this student's progress and recommend next steps:
        
        Student Profile: {student_profile}
        Learning History: {learning_history}
        Current Performance: {current_performance}
        
        Provide a comprehensive progress assessment including:
        1. Analysis of learning trajectory and growth
        2. Identification of strengths and areas for improvement
        3. Comparison with expected progress for this student's profile
        4. Recommendations for teaching strategy adjustments
        5. Suggestions for additional support or enrichment
        6. Timeline for next assessment or re-screening
        
        Ensure recommendations are specific, actionable, and tailored to this student.
        """

        return self.agent, prompt

    def get_agent(self):
        """Return the underlying Agent instance."""
        return self.agent
