import color_time

def sort_lessons(lessons_raw):
    colors = []
    max_color = -1
    for lesson in lessons_raw:
        if lesson['color'] > max_color:
            max_color = lesson['color']
    
    for i in range(max_color + 1):
        colors.append([])
    
    for lesson in lessons_raw:
        colors[lesson['color']].append(lesson)

    return colors

def assemble_lessons(result1, result2):
    if result1["order"] == 1:
        lessons1 = result1["events"]
        max1 = result1["number_of_colors"]
        lessons2 = result2["events"]
        max2 = result2["number_of_colors"]
    else:
        lessons1 = result2["events"]
        max1 = result2["number_of_colors"]
        lessons2 = result1["events"]
        max2 = result1["number_of_colors"]
    # the beginning timeslot of the 2. subset of lectures should be the first timeslot in the new day 
    # in order for the condition that no group or teacher has to attend more than 4 lectures per day to work 
    if max1 % 5 != 0:
        max1 += 5 - max1 % 5
    
    result = {}
    for lesson in lessons2:
        lesson["color"] += max1
        lessons1.append(lesson)
    
    color_to_time = color_time.color_to_time(max1 + max2)
    
    for lesson in lessons1:
        lesson["occurringTime"] = color_to_time[lesson["color"]]
    result['events'] = sort_lessons(lessons1)
    result["teachers"] = result1["teachers"]
    result["groups"] = result1["groups"]
    result["classrooms"] = result1["classrooms"]
    
    return result