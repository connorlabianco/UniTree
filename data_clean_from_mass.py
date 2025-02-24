import json
import re

# Load JSON data
with open('filtering.json', 'r') as f:
    data = json.load(f)

# Regex pattern to match:
# 1. Course codes (e.g., "THTDA 5", "PHYS 5", "PSTAT 120A-B-C")
# 2. Logical operators (and/or)
pattern = re.compile(
    r'\b([A-Z]+ \d+[A-Z-]*)\b|\b(and|or)\b',
    re.IGNORECASE
)

def clean_formatted_prerequisite(prereq):
    # Find all matches (course codes and operators)
    matches = pattern.findall(prereq)
    # Extract parts (flatten matches)
    parts = []
    for match in matches:
        if match[0]:  # Course code (e.g., "THTDA 5")
            parts.append(match[0].upper())
        elif match[1]:  # Operator (AND/OR)
            parts.append(match[1].upper())
    # Join with spaces
    return ' '.join(parts)

# Clean the formatted_prerequisite for each entry
for entry in data:
    if 'processedPrerequisites' in entry:
        original = entry['processedPrerequisites']
        original = original.replace('&', 'AND')
        cleaned = clean_formatted_prerequisite(original)
        if cleaned[-2:] == "OR":
            cleaned = cleaned[:-2]
        if cleaned[-3:] == "AND":
            cleaned = cleaned[:-3]
        if cleaned[-1:] == " ":
            cleaned = cleaned[:-1]
        entry['processedPrerequisites'] = cleaned

# Save to a new JSON file
with open('cleaned_data.json', 'w') as f:
    json.dump(data, f, indent=4)
