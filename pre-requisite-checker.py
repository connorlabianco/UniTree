import json
from collections import deque

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r") as file:
        return json.load(file)

def extract_prerequisites(cleaned_data):
    """Extract prerequisite relationships from cleaned_data.json."""
    prerequisites = {}
    for course in cleaned_data:
        course_code = course["courseCode"]
        prereqs = course.get("processedPrerequisites", "")
        if prereqs:
            prerequisites[course_code] = [prereq.strip() for prereq in prereqs.split(",")]
        else:
            prerequisites[course_code] = []
    return prerequisites

def combine_data(majors, prerequisites):
    """Combine majors data with prerequisite relationships."""
    combined_data = {}
    for major, details in majors.items():
        required_courses = details["required_courses"]
        for category, courses in required_courses.items():
            for course in courses:
                course_code = course[0]
                if course_code in prerequisites:
                    combined_data[course_code] = prerequisites[course_code]
                else:
                    combined_data[course_code] = []
    return combined_data

def build_graph_and_indegree(data):
    """Constructs the course prerequisite graph and computes in-degrees."""
    graph = {}
    in_degree = {}
    
    all_courses = set(data.keys()).union(*data.values())
    for course in all_courses:
        graph[course] = []
        in_degree[course] = 0
    
    for course, prereqs in data.items():
        for prereq in prereqs:
            graph[prereq].append(course)
            in_degree[course] += 1
    
    return graph, in_degree

def schedule_courses(data, majors, max_units_per_term=15):
    """Schedules courses into terms, prioritizing required courses and limiting units."""
    graph, in_degree = build_graph_and_indegree(data)
    schedule = []
    
    # Separate required and elective courses
    required_courses = set()
    for major, details in majors.items():
        for category, courses in details["required_courses"].items():
            for course in courses:
                required_courses.add(course[0])
    
    queue = deque([course for course, deg in in_degree.items() if deg == 0])
    
    while queue:
        term_courses = []
        term_units = 0
        
        # Prioritize required courses
        required_in_queue = [course for course in queue if course in required_courses]
        for course in required_in_queue:
            if term_units >= max_units_per_term:
                break
            term_courses.append(course)
            term_units += get_course_units(majors, course)
            queue.remove(course)
        
        # Add elective courses if there's room
        for course in list(queue):
            if term_units >= max_units_per_term:
                break
            term_courses.append(course)
            term_units += get_course_units(majors, course)
            queue.remove(course)
        
        # Update in-degrees for dependent courses
        for course in term_courses:
            for dependent in graph[course]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        schedule.append(term_courses)
    
    return schedule

def get_course_units(majors, course_code):
    """Get the number of units for a course from majors.json."""
    for major, details in majors.items():
        for category, courses in details["required_courses"].items():
            for course in courses:
                if course[0] == course_code:
                    return course[1]
    return 0  # Default to 0 if course not found

if __name__ == "__main__":
    # Load the JSON files
    majors = load_json("majors.json")
    cleaned_data = load_json("cleaned_data.json")
    
    # Extract prerequisite relationships
    prerequisites = extract_prerequisites(cleaned_data)
    
    # Combine majors data with prerequisites
    combined_data = combine_data(majors, prerequisites)
    
    # Schedule the courses
    schedule = schedule_courses(combined_data, majors, max_units_per_term=15)
    
    # Return term1
    term1 = schedule[0] if schedule else []
    print("Term 1 Courses:", term1)
