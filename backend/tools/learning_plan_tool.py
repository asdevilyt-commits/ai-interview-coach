from langchain_core.tools import tool


@tool
def create_learning_plan(topic: str) -> str:
    """Create an interview preparation learning plan for a given topic."""

    return f"""
Learning Plan for {topic}

1. Core Fundamentals
   - Syntax and basic concepts
   - Data types
   - Variables
   - Operators

2. Problem Solving
   - Conditions
   - Loops
   - Functions
   - Recursion

3. Data Structures
   - Lists
   - Tuples
   - Sets
   - Dictionaries

4. Advanced Python
   - OOP
   - Exceptions
   - Iterators
   - Generators
   - Decorators

5. Interview Practice
   - Python interview questions
   - Coding problems
   - Debugging exercises
   - Mock interview
"""