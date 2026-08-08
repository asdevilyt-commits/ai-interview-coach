import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.llm import ask_llm



def main():
    response = ask_llm(
        "Explain what an AI agent is in one simple paragraph."
    )

    print("\nLLM Response:")
    print(response)


if __name__ == "__main__":
    main()