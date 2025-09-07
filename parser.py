import re
from typing import List, Dict
from models import Course, ClassOption

def normalize_input(text: str) -> str:
    """Normalize input by handling Persian/English numbers, commas, and dashes."""
    # Replace Persian numbers with English
    persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    text = text.translate(persian_to_english)
    # Normalize commas (Persian/English) and dashes
    text = re.sub(r'[،,]', ',', text)
    text = re.sub(r'[–—]', '-', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def normalize_time(time_str: str) -> str:
    """Normalize time format (e.g., '8' -> '08:00', '8:0' -> '08:00')."""
    time_str = time_str.strip()
    match = re.match(r'(\d{1,2})(?::(\d{1,2}))?', time_str)
    if not match:
        raise ValueError(f"Invalid time format: {time_str}")
    hour, minute = match.groups()
    hour = int(hour)
    minute = int(minute) if minute else 0
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Time out of range: {time_str}")
    return f"{hour:02d}:{minute:02d}"

def parse_courses(raw_input: str) -> List[Course]:
    """
    Parse raw user input into a list of Course objects.

    Expected input format per line:
    درس - استاد - روز شروع الی پایان، [روز شروع الی پایان، ...] - واحد

    Example:
    ریاضی - محمدی - دوشنبه ۱۴:۰۰ الی ۱۵:۳۰، سه شنبه ۱۴:۰۰ الی ۱۵:۳۰ - ۳
    """
    courses_dict: Dict[str, Dict] = {}  # temporary structure
    valid_days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']

    for line_num, line in enumerate(raw_input.splitlines(), start=1):
        line = normalize_input(line)
        if not line:
            continue

        try:
            # Split into parts: [name, teacher, times, credits]
            parts = [p.strip() for p in line.split(" - ")]
            if len(parts) != 4:
                raise ValueError(f"Invalid format in line {line_num}: {line}")

            name, teacher, times_str, credits_str = parts

            # Extract credits (handle '3 واحد' or '۳')
            credits_match = re.match(r'(\d+)(?:\s*واحد)?$', credits_str.strip())
            if not credits_match:
                raise ValueError(f"Invalid credits format in line {line_num}: {credits_str}")
            credits = int(credits_match.group(1))

            # Parse multiple times (separated by ",")
            times = []
            for time_block in times_str.split(","):
                time_block = time_block.strip()
                match = re.match(r"(.+?)\s+(\d{1,2}(?::\d{1,2})?)\s+الی\s+(\d{1,2}(?::\d{1,2})?)", time_block)
                if not match:
                    raise ValueError(f"Invalid time block format in line {line_num}: {time_block}")
                day, start, end = match.groups()
                day = day.strip()
                start = normalize_time(start)
                end = normalize_time(end)
                # Validate day
                if day not in valid_days:
                    raise ValueError(f"Invalid day in line {line_num}: {day}")
                times.append((day, start, end))

            class_option = ClassOption(teacher, times)

            # Add to dictionary
            if name not in courses_dict:
                courses_dict[name] = {"credits": credits, "options": []}
            courses_dict[name]["options"].append(class_option)

        except Exception as e:
            raise ValueError(f"Error in line {line_num}: {line}\n{e}")

    # Convert dictionary to list of Course objects
    courses = []
    for name, data in courses_dict.items():
        courses.append(Course(name, data["credits"], data["options"]))

    return courses