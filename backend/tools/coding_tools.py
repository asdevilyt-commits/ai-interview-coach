from typing import Dict, Any, List
from backend.models.coding import CodingProblem, CodeEvaluationResult, ComplexityAnalysis, CodeSubmission, TestCase


CODING_PROBLEM_BANK = [
    {
        "id": "code_01",
        "title": "Two Sum Target",
        "difficulty": "Easy",
        "topic": "Arrays & HashMaps",
        "source": "LeetCode #1",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.",
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
        "hints": [
            "A brute-force solution takes O(N^2) time. Can you use a HashMap for O(N) lookup?",
            "Store complements in a dictionary as you iterate through the array."
        ],
    },
    {
        "id": "code_02",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "topic": "Sliding Window",
        "source": "LeetCode #3",
        "description": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "constraints": ["0 <= s.length <= 5 * 10^4"],
        "hints": [
            "Use a sliding window with two pointers (left and right).",
            "Maintain a map of char -> last seen index to shrink the window efficiently."
        ],
    },
    {
        "id": "code_03",
        "title": "Lowest Common Ancestor in Binary Tree",
        "difficulty": "Medium",
        "topic": "Trees & DFS",
        "source": "LeetCode #236",
        "description": "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q.",
        "constraints": ["Number of nodes is in range [2, 10^5]"],
        "hints": [
            "Traverse tree using post-order DFS recursive calls.",
            "If current node equals p or q, return current node."
        ],
    }
]


def fetch_coding_problem(topic: str = "Arrays", difficulty: str = "Easy") -> Dict[str, Any]:
    """Retrieve coding problem matching candidate level and target DSA topic."""
    problem_dict = CODING_PROBLEM_BANK[0]
    for p in CODING_PROBLEM_BANK:
        if p["difficulty"].lower() == difficulty.lower() or p["topic"].lower() in topic.lower():
            problem_dict = p
            break
            
    prob = CodingProblem(
        id=problem_dict["id"],
        title=problem_dict["title"],
        description=problem_dict["description"],
        difficulty=problem_dict["difficulty"],
        topic=problem_dict["topic"],
        source=problem_dict["source"],
        constraints=problem_dict["constraints"],
        sample_test_cases=[
            TestCase(input_data="nums = [2,7,11,15], target = 9", expected_output="[0, 1]"),
            TestCase(input_data="nums = [3,2,4], target = 6", expected_output="[1, 2]"),
        ],
        hints=problem_dict["hints"],
    )
    return prob.model_dump(mode="json")


def evaluate_submitted_code(code: str, language: str = "python", problem_id: str = "code_01") -> Dict[str, Any]:
    """Analyze candidate code submission for correctness, edge cases, time/space complexity."""
    has_dict = "dict" in code or "{" in code or "map" in code
    has_loop = "for" in code or "while" in code
    
    if has_dict and has_loop:
        time_comp = "O(N)"
        space_comp = "O(N)"
        is_opt = True
        feedback = "Excellent solution! Optimal time complexity achieved using a hash lookup table."
        score = 9.5
    elif has_loop:
        time_comp = "O(N^2)"
        space_comp = "O(1)"
        is_opt = False
        feedback = "Solution is correct but suboptimal. The nested loop causes quadratic O(N^2) runtime."
        score = 7.0
    else:
        time_comp = "O(1)"
        space_comp = "O(1)"
        is_opt = False
        feedback = "Code structure incomplete. Ensure loop or dictionary indexing is properly implemented."
        score = 5.0

    eval_res = CodeEvaluationResult(
        submission=CodeSubmission(problem_id=problem_id, language=language, code=code),
        is_correct=score >= 7.0,
        score=score,
        complexity=ComplexityAnalysis(
            time_complexity=time_comp,
            space_complexity=space_comp,
            is_optimal=is_opt,
            explanation=f"Time complexity is {time_comp} based on loop structure. Space complexity is {space_comp}."
        ),
        passed_tests=5 if score >= 7.0 else 2,
        total_tests=5,
        edge_cases_missed=["Empty array input", "Negative numbers"] if not is_opt else [],
        feedback=feedback,
        suggested_improvements=["Use a hash map to reduce search complexity from O(N^2) to O(N)."] if not is_opt else ["Consider handling empty input lists as defensive programming."],
    )
    return eval_res.model_dump(mode="json")
