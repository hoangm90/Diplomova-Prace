from typing import Optional
import get_data

def sort_lessons(group_id: Optional[str] = None, teacher_id: Optional[str] = None, classroom_id: Optional[str] = None):
    lessons = get_data.get_lessons_with_names()
    colors = []
    max_color = -1
    for lesson in lessons:
        if lesson['color'] > max_color:
            max_color = lesson['color']
    
    for i in range(max_color + 1):
        colors.append([])
    
    for lesson in lessons:
        if classroom_id == None or classroom_id == lesson["chosen_classroom_id"]:
            if group_id == None or group_id in lesson["group_ids"]:
                if teacher_id == None or teacher_id in lesson["teacher_ids"]:
                    colors[lesson['color']].append(lesson)

    return colors

if __name__ == "__main__":
    colors = sort_lessons()
    print(colors[3038])