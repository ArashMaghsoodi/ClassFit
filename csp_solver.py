from typing import List, Dict
from models import Course, ClassOption

def schedules_conflict(option1: ClassOption, option2: ClassOption) -> bool:
    """
    Check if two class options conflict in time.
    """
    for day1, start1, end1 in option1.times:
        for day2, start2, end2 in option2.times:
            if day1 == day2 and not (end1 <= start2 or end2 <= start1):
                return True
    return False

def solve_all_schedules(courses: List[Course]) -> List[Dict[str, ClassOption]]:
    """
    Backtracking CSP solver that finds ALL valid schedules without conflicts.
    Returns a list of possible assignments, sorted by total priority.
    """
    solutions = []

    def backtrack(assignment: Dict[str, ClassOption], index: int):
        if index == len(courses):
            solutions.append(assignment.copy())
            return

        course = courses[index]
        for option in course.options:
            conflict = any(
                schedules_conflict(option, assigned_option)
                for assigned_option in assignment.values()
            )
            if not conflict:
                assignment[course.name] = option
                backtrack(assignment, index + 1)
                del assignment[course.name]

    backtrack({}, 0)

    # Sort solutions by total priority (sum of priorities of selected options)
    solutions.sort(key=lambda s: -sum(opt.priority for opt in s.values()))

    return solutions