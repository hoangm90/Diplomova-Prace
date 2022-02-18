def return_planned_timetables(data, colors, chosen_classrooms, max_color):
    dict_classrooms = {}
    for cl in data["classrooms"]:
        dict_classrooms[cl["id"]] = cl["name"]

    lessons_raw = data["events"]
    for l in lessons_raw:
        id = l["id"]
        l["color"] = colors[id]
        l["chosenClassroomId"] = chosen_classrooms[id]
        l["chosenClassroom"] = dict_classrooms.get(l["chosenClassroomId"]) if dict_classrooms.get(l["chosenClassroomId"]) != None else ""
    
    result = data
    result["events"] = lessons_raw
    result["number_of_colors"] = max_color + 1
    return result