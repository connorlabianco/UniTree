import json
import re

# def extract_course_prefix(course_code):
#     """Extracts the alphabetic prefix from a course code."""
#     match = re.match(r'([A-Za-z]+)', course_code)
#     return match.group(1).upper() if match else ""

# def clean_prerequisite(prereq, course_prefix):
#     """
#     Cleans prerequisite entries:
#     - Removes extra words before actual course codes.
#     - Ensures only valid course codes remain.
#     - Removes phrases like 'consent of instructor' or similar.
#     """


#     # Ensure it starts with the proper prefix if missing
#     if not re.match(r'^[A-Za-z]+', prereq):
#         prereq = f"{course_prefix}{prereq}"
    
#     # Remove trailing periods (e.g., "ANTH100.")
#     prereq = prereq.rstrip(".")

#     prereq = re.sub(r'(\d+[A-Z]?)(.*?)\s*$', r'\1', prereq)

#     return prereq.upper()

# def extract_prereqs(str, course_prefix):
#     # find all instances of course codes
#     prereq_list = re.findall(r"[a-zA-Z]+\s?[0-9]+[A-C]*", str)

#     # remove any unneeded trailing string
#     str = re.sub(r'(\d+[A-Z]?)(.*?)\s*$', r'\1', str)
#     return prereq_list

def parse_requisites(req_string, course_prefix):
    """Parses requisites string into a structured format."""
    if not req_string:
        return []
    
    parts = [p.strip() for p in req_string.split(';') if p.strip()]
    result = []
    
    for part in parts:
        if ' or ' in part.lower():
            options = [opt.strip() for opt in re.split(r'\bor\b', part, flags=re.IGNORECASE)]
            # cleaned_options = [extract_prereqs(opt, course_prefix) for opt in options] # type: ignore
            # result.append(cleaned_options)
        else:
            result.append((part, course_prefix)) # type: ignore
    
    return result

def extract_course_requisites_large(input_file_path, output_file_path):
    """Extracts and processes course requisites from a large JSON file efficiently."""
    try:
        result = {}

        with open(input_file_path, 'r', encoding="UTF-8") as f:
            courses = json.load(f)  # Load as a dictionary
        
        for course_id, course_data in courses.items():
            code = course_data.get('code', '').strip()
            if not code:
                continue

            course_prefix = (code)  # type: ignore # Dynamically determine prefix

            requisites = course_data.get('requisites', {})
            freeform = requisites.get('requisitesFreeform', {})
            req_value = freeform.get('value', '').strip()
            
            result[code] = parse_requisites(req_value, course_prefix)

        # Write output to JSON file
        with open(output_file_path, 'w', encoding="UTF-8") as out_f:
            json.dump(result, out_f, indent=2)

        print(f"Successfully created {output_file_path}")

    except Exception as e:
        print(f"Unexpected error: {e}")

# Example Usage
extract_course_requisites_large('courses.json', 'course_requisites.json')

