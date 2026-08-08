import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.agent_graph import build_interview_graph



def main():

    graph = build_interview_graph()

    initial_state = {
        "user_request": "Prepare me for a Python interview",
        "candidate_id": "test_candidate"
    }

    result = graph.invoke(initial_state)

    print("\nFinal State:")
    print(result)


if __name__ == "__main__":
    main()