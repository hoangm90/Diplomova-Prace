import random_sorting

def coloring(subjects, lessons, groups, teachers, classrooms, G):
    [nodes, dict_previous_lesson] = random_sorting.random_sorting(subjects)
    # create the dictionary with keys are lessons
    # and values are color assigning to each lesson,
    # and classroom assigning to each lesson
    colors = {}
    chosen_classroom = {}

    # track the highest color
    max_color = -1
    
    # create a dictionary to track if a classroom is available
    # in a specific timeslots
    classroom_available = {}
    for classroom in classrooms:
        classroom_available[classroom["id"]] = {}
    
    # create group dict and teacher dict to track the number of lectures they attend in each day
    teachers_dict = {}
    for te in teachers:
        teachers_dict[te["id"]] ={}
    
    groups_dict = {}
    for gr in groups:
        groups_dict[gr["id"]] = {}
    
    for node in nodes:
        current_lesson = lessons[node]
        #create a set of colors that is not available for this node,
        # which contains colors of neighbor nodes
        colors_not_avai = {colors[v] for v in G[node] if v in colors} 
        # find the smallest available for this node
        
        if dict_previous_lesson[node] == 0:
            color = 0
        else:
            color = colors[dict_previous_lesson[node]] + 1
       
        while True:
            # test to see if the color is in the set of unavaiable colors 
            if color not in colors_not_avai:
                can_assign = True
                # if the teachers are available at this color
                for teacher_id in current_lesson['teacherIDs']:
                    if teachers_dict[teacher_id].get(color//5) == None:
                        teachers_dict[teacher_id][color//5] = 0
                    elif teachers_dict[teacher_id][color//5] == 4:
                        can_assign = False
                        break
                    
                if not can_assign:
                    color += 1
                    continue
                # if the groups are available at this color
                for group_id in current_lesson['groupIDs']:
                    if groups_dict[group_id].get(color//5) == None:
                        groups_dict[group_id][color//5] = 0
                    elif groups_dict[group_id][color//5] == 4:
                        can_assign = False
                        break

                if not can_assign:
                    color += 1
                    continue
                # if the color is not in the set, then test to see if 
                # there is available room for this lesson at this color(timeslot)
                if len(current_lesson['classroomIDs']) == 0:
                    chosen_classroom[node] = ""
                    break
                else:
                    can_assign_classroom = False
                    for classroom_id in current_lesson['classroomIDs']:
                        if classroom_id == 1280 or classroom_id == 1281 or classroom_id == 1284:
                            chosen_classroom[node] = classroom_id
                            can_assign_classroom = True
                    if can_assign_classroom == False:
                        for classroom_id in current_lesson['classroomIDs']:
                            if classroom_available[classroom_id].get(color) == None:
                            # if the is available room, assign that room to this lesson and break the loop
                                classroom_available[classroom_id][color] = True
                                chosen_classroom[node] = classroom_id
                                can_assign_classroom = True
                                break

                    if can_assign_classroom:
                        break
                # if the considered color is not available, raise it for 1 
            color += 1
        # assign the available color(timeslot) to the node(lession)
        colors[node] = color
        # track the max color
        if color > max_color:
            max_color = color
        # track the number of lectures teachers teach in one day
        for teacher_id in current_lesson['teacherIDs']:
            teachers_dict[teacher_id][color//5] += 1
        # track the number of lectures groups attend in one day
        for group_id in current_lesson['groupIDs']:
            groups_dict[group_id][color//5] += 1
    
    result = {}
    result["colors"] = colors
    result["chosen_classrooms"] = chosen_classroom
    result["max_color"] = max_color

    return result