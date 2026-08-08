import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.agents.agent import AgentState, InterviewAgent



def main():
    agent = InterviewAgent()

    state = AgentState(
        goal="I want to prepare for my interview"
    )

    state = agent.decide(state)

    print("Goal:", state.goal)
    print("Agent decided:", state.action)

    state = agent.execute(state)

    print("Result:", state.result)


if __name__ == "__main__":
    main()