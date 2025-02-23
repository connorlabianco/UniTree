#!/usr/bin/env python
# coding: utf-8

# In[5]:


import re

def parse_prerequisites(prereq_text):
    """
    Recursively parses pre-requisite text using regex and pattern matching.
    
    Args:
        prereq_text (str): The raw pre-requisite text.
    
    Returns:
        list: Parsed pre-requisite structure in a hierarchical list format.
    """
    patterns = {
        "course_list_comma": re.compile(r"([A-Z]+\s*\d+[A-Z]*)(,\s*)"),  # WRIT502C, WRIT503, WRIT504
        "course_list_and/or": re.compile(r"([A-Z]+\s*\d+[A-Z]*)(((\s(and|or)\s)([A-Z]+\s*\d+[A-Z]*))+)"),  # WRIT502C and WRIT503
        "course_series": re.compile(r"([A-Z]+)\s*(\d+)([A-Z]+)([-]([A-Z]+))*"),  # MATH101A, ..., MATH101C
        "course_num_str": re.compile(r"([A-Z]+\s*\d+[A-Z]*)[.]+"),  # WRIT502C and WRIT503
        "int_str_title": re.compile(r"(\d+)\s*(.*?)\s*\[([^\]]+)\]"),  # 3 credits in [Title]
        "course_num": re.compile(r"([A-Z]+\s*\d+[A-Z]*)"),  # WRIT 502C
        "course": re.compile(r"([A-Z]+)"),  # WRIT
        "none": re.compile(r"(?i)\b(no prerequisites|none|not required)\b"),  # No prerequisites
    }

    def recursive_parse(text):
        """
        Recursively parse the text and extract course codes and logical relationships.
        """
        text = text.strip()

        for case, pattern in patterns.items():
            match = pattern.search(text)
            if match:
                print(case)
                print("match:", match.group())
                # and/or case
                if case in ["course_list_and/or"]:
                    # Handle logical groupings (e.g., "WRIT502C and WRIT503")
                    print("and/or case")
                    first = re.search(r"([A-Z]+\s*\d+[A-Z]*)", text)
                    courses = match.group().replace(first.group()+" ", "")
                    print("remaining text:", courses)
                    
                    and_ors = re.findall(r'\b(and|or)\b', courses)
                    
                    logical_operator = "AND" if and_ors[0] == "and" else "OR"
                    
                    first = [first.group()]
                    and_combined = first + recursive_parse(courses)
                    print("combination:", and_combined)
                        
                    if logical_operator == "AND":
                        return and_combined
                    elif logical_operator == "OR":
                        first_and = and_ors.index("and")
                        or_segment = and_combined[:first_and]
                        #and_segment = and_combined[first_and:]
                        return ["/".join(or_segment)]
                elif case in ["course_num", "course_series", "course_series_shorthand", "course_num_str"]:
                    print("course found")
                    return list(match.groups())
                elif case == "none":
                    return []  # No prerequisites

        return text  # Return text if nothing matches

    parsed_data = recursive_parse(prereq_text)
    return parsed_data


# In[4]:


#prereq_example = "WRIT502C, WRIT503, WRIT504 or MATH101A and MATH101B and MATH101C. Upper-division standing required."
prereq_example = "MDCB 1A, 2B, 3D"
parsed_output = parse_prerequisites(prereq_example)
print(parsed_output)

