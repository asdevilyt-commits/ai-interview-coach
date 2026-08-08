from dataclasses import dataclass


@dataclass
class AgentState:
    goal: str
    action = None
    result = None


class InterviewAgent:

    def decide(self, state: AgentState) -> AgentState:
        """
        Decide what the agent should do based on the user's goal.
        """

        if "resume" in state.goal.lower():
            state.action = "analyze_resume"

        elif "interview" in state.goal.lower():
            state.action = "start_interview"

        else:
            state.action = "ask_clarification"

        return state

    def execute(self, state: AgentState) -> AgentState:
        """
        Execute the action selected by the agent.
        """

        if state.action == "analyze_resume":
            state.result = "Resume analysis should be performed."

        elif state.action == "start_interview":
            state.result = "Interview preparation should be started."

        elif state.action == "ask_clarification":
            state.result = "Need more information from the candidate."

        return state