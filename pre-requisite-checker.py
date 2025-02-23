import json
from collections import deque

def standardize_course_id(course):
    """Standardize course ID by removing spaces."""
    return course.replace(" ", "")

def build_graph_and_indegree(data):
    """Constructs the course prerequisite graph and computes in-degrees."""
    std_data = {
        standardize_course_id(course): [standardize_course_id(p) for p in prereqs]
        for course, prereqs in data.items()
    }
    
    graph = {}
    in_degree = {}
    
    all_courses = set(std_data.keys()).union(*std_data.values())
    for course in all_courses:
        graph[course] = []
        in_degree[course] = 0
    
    for course, prereqs in std_data.items():
        for prereq in prereqs:
            graph[prereq].append(course)
            in_degree[course] += 1
    
    return graph, in_degree

def schedule_courses(data, max_per_term=4):
    """Schedules courses into terms using BFS topological sort."""
    graph, in_degree = build_graph_and_indegree(data)
    schedule = []
    
    queue = deque([course for course, deg in in_degree.items() if deg == 0])
    
    while queue:
        term_courses = [queue.popleft() for _ in range(min(len(queue), max_per_term))]
        
        for course in term_courses:
            for dependent in graph[course]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        schedule.append(term_courses)
    
    return schedule

if __name__ == "__main__":
    # Read the course data from JSON
    with open("course_data.json", "r") as file:
        data = json.load(file)

    schedule = schedule_courses(data, max_per_term=4)

    print("\nCourse Schedule (Max 4 courses per term):")
    for term_idx, courses in enumerate(schedule, start=1):
        print(f"Term {term_idx}: {courses}")
