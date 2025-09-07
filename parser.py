import re
from typing import List, Dict
from models import Course, ClassOption

def parse_courses(raw_input: str) -> List[Course]:
    """
    Parse raw user input into a list of Course objects.
    
    Expected input format per line:
    درس - استاد - روز شروع الی پایان، [روز شروع الی پایان، ...] - واحد

    Example:
    ریاضی - محمدی - دوشنبه ۱۴:۰۰ الی ۱۵:۳۰، سه شنبه ۱۴:۰۰ الی ۱۵:۳۰ - ۳
    """

    courses_dict: Dict[str, Dict] = {}  # temporary structure

    for line in raw_input.splitlines():
        line = line.strip()
        if not line:
            continue

        try:
            # Split into parts: [name, teacher, times, credits]
            parts = [p.strip() for p in line.split(" - ")]
            if len(parts) != 4:
                raise ValueError(f"Invalid format: {line}")

            name, teacher, times_str, credits_str = parts
            credits = int(credits_str)

            # Parse multiple times (separated by "،")
            times = []
            for time_block in times_str.split("،"):
                time_block = time_block.strip()
                match = re.match(r"(.+?)\s+(\d{1,2}:\d{2})\s+الی\s+(\d{1,2}:\d{2})", time_block)
                if not match:
                    raise ValueError(f"Invalid time format: {time_block}")
                day, start, end = match.groups()
                times.append((day.strip(), start, end))

            class_option = ClassOption(teacher, times)

            # Add to dictionary
            if name not in courses_dict:
                courses_dict[name] = {"credits": credits, "options": []}
            courses_dict[name]["options"].append(class_option)

        except Exception as e:
            raise ValueError(f"Error parsing line: {line}\n{e}")

    # Convert dictionary to list of Course objects
    courses = []
    for name, data in courses_dict.items():
        courses.append(Course(name, data["credits"], data["options"]))

    return courses