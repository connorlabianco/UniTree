from datetime import datetime

class_data = [
    {"name": "CS 156", "units": 4, "time": "10:00am-11:00am"},
    {"name": "CS 170", "units": 4, "time": "6:00pm-7:30pm"},
    {"name": "CS 170", "units": 4, "time": "4:00pm-5:30pm"},
    {"name": "CS 170", "units": 4, "time": "2:00pm-3:30pm"}
]

# block that breaks what would have been a potential schedule input and converts the string times into comparable times.
classtimes = []
classtimes24hr = []
# splits the time into a format that the code can understand.
for course in class_data:
    course['time'] = course['time'].split('-')
for course in class_data:
    temp = []
    time = None
    # part that actually converts the sting 12hr representation into the 24hr comparable representation.
    for i in range(2):
        time = datetime.strptime(course['time'][i], "%I:%M%p")
        time = time.strftime("%H:%M")
        course['time'][i] = time
    classtimes24hr.append(temp)
    # sorts the time data based on the new 24hr representations.
for course in class_data:
    class_data = sorted(class_data, key=lambda x: x['time'])

# checks to see that the different times are not overlapping or equal in start time
i = 1
for course in class_data:
    start = course['time'][0]
    temp = course['time'][i]
    if start >= temp:
        print("start times overlap or are equal.", start, temp)
    start = temp
    i += 1
    if i >= len(class_data) - 2:
        break

# checks to see if the end times overlap with the start times of the classes.
i = 1
for course in class_data:
    end = course['time'][0]
    beg = course['time'][1]
    while course['time']:
        if end >= beg:
            print("overlapping end times.", end, beg)
        end = course['time'][1]
        i += 1
        if i >= len(course['time']):
            break
        beg = course['time'][0]

