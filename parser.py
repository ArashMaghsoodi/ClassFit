import re
import logging
from typing import List, Dict, Tuple
from models import Course, ClassOption

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def normalize_input(text: str) -> str:
    """Normalize input by handling Persian/English numbers, commas, and dashes."""
    persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    text = text.translate(persian_to_english)
    text = re.sub(r'[،,]', '،', text)  # Normalize to Persian comma
    text = re.sub(r'[–—]', '-', text)
    text = re.sub(r'\s+', ' ', text.strip())
    logging.debug(f"Normalized input: {text}")
    return text

def normalize_time(time_str: str) -> str:
    """Normalize time format (e.g., '8' -> '08:00', '8:0' -> '08:00')."""
    time_str = time_str.strip()
    logging.debug(f"Normalizing time: {time_str}")
    match = re.match(r'(\d{1,2})(?::(\d{1,2}))?', time_str)
    if not match:
        raise ValueError(f"Invalid time format: {time_str}")
    hour, minute = match.groups()
    hour = int(hour)
    minute = int(minute) if minute else 0
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Time out of range: {time_str}")
    return f"{hour:02d}:{minute:02d}"

def parse_courses(raw_input: str) -> Tuple[List[Course], Dict[str, Dict[str, int]]]:
    """
    Parse raw user input into a list of Course objects and priority preferences.

    Expected input format per line:
    درس - استاد - روز شروع الی پایان، [روز شروع الی پایان، ...] - واحد
    OR
    اولویت: درس - استاد

    Example:
    سیگنال - حسینی - یکشنبه ۷:۴۵ الی ۹:۱۵، سه‌شنبه ۷:۴۵ الی ۹:۱۵ - ۳
    اولویت: سیگنال - حسینی
    """
    courses_dict: Dict[str, Dict] = {}  # temporary structure
    valid_days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
    priorities: Dict[str, Dict[str, int]] = {}  # course_name -> {teacher: priority}
    priority_counter = 0  # To assign increasing priorities (first has highest)

    # First pass: parse all lines to collect priorities and courses
    for line_num, line in enumerate(raw_input.splitlines(), start=1):
        line = normalize_input(line)
        if not line:
            continue

        logging.debug(f"Processing line {line_num}: {line}")

        try:
            if line.startswith("اولویت:"):
                # Parse priority
                priority_content = line[7:].strip()  # Remove "اولویت:"
                parts = [p.strip() for p in priority_content.split(" - ")]
                if len(parts) != 2:
                    raise ValueError(f"Invalid priority format in line {line_num}: {priority_content}")
                course, teacher = parts
                course = course.strip()
                teacher = teacher.strip()
                if course not in priorities:
                    priorities[course] = {}
                priorities[course][teacher] = priority_counter + 1
                priority_counter += 1
                logging.debug(f"Added priority: {course} -> {teacher} (priority {priorities[course][teacher]})")
                continue

            # Parse course
            parts = [p.strip() for p in line.split(" - ")]
            if len(parts) != 4:
                raise ValueError(f"Invalid format in line {line_num}: {line}")

            name, teacher, times_str, credits_str = parts
            name = name.strip()
            teacher = teacher.strip()
            logging.debug(f"Parsed course: name={name}, teacher={teacher}, times={times_str}, credits={credits_str}")

            # Extract credits
            credits_match = re.match(r'(\d+)(?:\s*واحد)?$', credits_str.strip())
            if not credits_match:
                raise ValueError(f"Invalid credits format in line {line_num}: {credits_str}")
            credits = int(credits_match.group(1))

            # Parse times
            times = []
            for time_block in times_str.split("،"):
                time_block = time_block.strip()
                logging.debug(f"Processing time block: {time_block}")
                match = re.match(r"(.+?)\s+(\d{1,2}:\d{2})\s+الی\s+(\d{1,2}:\d{2})", time_block)
                if not match:
                    raise ValueError(f"Invalid time block format in line {line_num}: {time_block}")
                day, start, end = match.groups()
                day = day.strip()
                start = normalize_time(start)
                end = normalize_time(end)
                if day not in valid_days:
                    raise ValueError(f"Invalid day in line {line_num}: {day}")
                times.append((day, start, end))

            # Create ClassOption with default priority 0 (will update later)
            class_option = ClassOption(teacher, times, 0)

            # Add to dictionary
            if name not in courses_dict:
                courses_dict[name] = {"credits": credits, "options": []}
            courses_dict[name]["options"].append(class_option)

        except Exception as e:
            logging.error(f"Error in line {line_num}: {line}\n{e}")
            raise ValueError(f"Error in line {line_num}: {line}\n{e}")

    # Second pass: update priorities for all ClassOptions
    for name, data in courses_dict.items():
        for option in data["options"]:
            option.priority = priorities.get(name, {}).get(option.teacher, 0)
            logging.debug(f"Updated priority for {name} -> {option.teacher}: {option.priority}")

    # Convert dictionary to list of Course objects
    courses = []
    for name, data in courses_dict.items():
        courses.append(Course(name, data["credits"], data["options"]))
    logging.debug(f"Parsed courses: {courses}, priorities: {priorities}")

    return courses, priorities