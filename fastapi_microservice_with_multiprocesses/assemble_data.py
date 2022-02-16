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

def assemble_lessons(arr1, arr2, data):
    lessons1 = arr1[0]
    max1 = arr1[1]
    lessons2 = arr2[0]
    max2 = arr2[1]
        
    result = {}
    for lesson in lessons2:
        lesson["color"] += max1
        lessons1.append(lesson)
    
    color_to_time = color_time.color_to_time(max1 + max2)
    
    for lesson in lessons1:
        lesson["occurringTime"] = color_to_time[lesson["color"]]
    result['events'] = sort_lessons(lessons1)
    result["teachers"] = data["teachers"]
    result["groups"] = data["groups"]
    result["classrooms"] = data["classrooms"]
    
    return result