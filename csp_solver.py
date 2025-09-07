from typing import List, Dict, Optional
from models import Course, ClassOption

def has_conflict(times1: List[tuple], times2: List[tuple]) -> bool:
    """Check if two class schedules conflict."""
    for day1, start1, end1 in times1:
        for day2, start2, end2 in times2:
            if day1 == day2:
                if not (end1 <= start2 or end2 <= start1):  # overlap check
                    return True
    return False


def solve_schedule(courses: List[Course]) -> Optional[Dict[str, ClassOption]]:
    """
    Try to assign one ClassOption to each Course without conflicts.
    Returns a dictionary {course_name: chosen_class_option} or None if impossible.
    """
    assignment: Dict[str, ClassOption] = {}

    def backtrack(index: int) -> bool:
        if index == len(courses):
            return True

        course = courses[index]
        for option in course.options:
            # Check conflict with already assigned classes
            conflict = False
            for chosen in assignment.values():
                if has_conflict(option.times, chosen.times):
                    conflict = True
                    break
            if conflict:
                continue

            # Assign and recurse
            assignment[course.name] = option
            if backtrack(index + 1):
                return True
            del assignment[course.name]  # undo

        return False

    if backtrack(0):
        return assignment
    return None