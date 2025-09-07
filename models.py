from typing import List, Tuple

class ClassOption:
    """
    Represents a single class option of a course (a specific teacher + schedule).
    """
    def __init__(self, teacher: str, times: List[Tuple[str, str, str]]):
        """
        :param teacher: Teacher's name (e.g. "محمدی")
        :param times: List of tuples (day, start_time, end_time)
                      Example: [("دوشنبه", "14:00", "15:30")]
        """
        self.teacher = teacher
        self.times = times

    def __repr__(self):
        return f"ClassOption(teacher={self.teacher}, times={self.times})"


class Course:
    """
    Represents a university course with multiple possible class options.
    """
    def __init__(self, name: str, credits: int, options: List[ClassOption]):
        """
        :param name: Course name (e.g. "ریاضی")
        :param credits: Number of credits (e.g. 3)
        :param options: List of ClassOption objects
        """
        self.name = name
        self.credits = credits
        self.options = options

    def __repr__(self):
        return f"Course(name={self.name}, credits={self.credits}, options={len(self.options)})"