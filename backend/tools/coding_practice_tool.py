from langchain_core.tools import tool


@tool
def create_coding_practice(topic: str) -> str:
    """Create coding interview practice for a given topic."""

    return f"""
Coding Practice Plan for {topic}

1. Basic Problems
   - Variables
   - Conditions
   - Loops

2. Data Structures
   - Lists
   - Dictionaries
   - Sets
   - Tuples

3. Algorithms
   - Searching
   - Sorting
   - Recursion

4. Interview Problems
   - Two Sum
   - Valid Parentheses
   - Palindrome
   - Binary Search

5. Practice Strategy
   - Solve without hints
   - Analyze complexity
   - Explain your solution
"""