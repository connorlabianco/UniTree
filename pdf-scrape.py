import pdfplumber
import re
import json

# Step 1: Extract text from the PDF
def extract_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Step 2: Extract course codes using regex
def parse_courses(text):
    # Regex to find course codes (e.g., CMPSC 16, MATH 3A)
    course_pattern = r'([A-Z]+\s*\d+[A-Z]*)'
    course_codes = re.findall(course_pattern, text)
    
    # Remove spaces and duplicates, sort alphabetically
    cleaned_course_codes = [course.replace(" ", "") for course in course_codes]
    unique_course_codes = sorted(set(cleaned_course_codes))
    return unique_course_codes

# Step 3: Load the prerequisites data from course_requisites.json
def load_prerequisites(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)

# Step 4: Create the course dictionary with prerequisites and other details
def map_courses_to_prerequisites(courses_list, requisites_data):
    courses_dict = {}
    
    for course in courses_list:
        # Check if the course exists in the requisites data, otherwise set prerequisites to an empty list
        prerequisites = requisites_data.get(course, [])
        
        # Add course to dictionary with prerequisites
        courses_dict[course] = prerequisites
        
    return courses_dict

# Step 5: Generate JSON structure for the course data and save it to course_data.json
def save_to_json(courses_dict, output_path):
    with open(output_path, 'w') as outfile:
        json.dump(courses_dict, outfile, indent=4)

# Step 6: Main function to run the whole process
def main(pdf_path, requisites_json_path, output_json_path):
    # Extract text from the PDF
    text = extract_pdf_text(pdf_path)
    
    # Parse course codes from the text
    course_codes = parse_courses(text)
    
    # Load prerequisites data from the JSON file
    requisites_data = load_prerequisites(requisites_json_path)
    
    # Map course codes to prerequisites and other details
    courses_dict = map_courses_to_prerequisites(course_codes, requisites_data)
    
    # Save the course data with prerequisites to course_data.json
    save_to_json(courses_dict, output_json_path)

# Run the script
pdf_path = "Computer Science - BS - 2024.pdf"  # Replace with your actual PDF file path
requisites_json_path = "course_requisites.json"  # Path to the course_requisites.json file
output_json_path = "course_data.json"  # Path to the output course_data.json file
main(pdf_path, requisites_json_path, output_json_path)
