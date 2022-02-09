import requests

def creat_time_table(url, filename):
    # send event file to micro service
    with open(filename, 'rb') as f:
        file = {"data": (f.name, f, "multipart/form-data")}
        r = requests.post(url=url, files=file)
    print(r.text)

####################################################################
def get_time_table(url, group_id, teacher_id, classroom_id):
    # get the time table with specific teacher, group and classroom
    parameter={}
    if group_id != "":
        parameter["group_id"] = group_id
    if teacher_id != "":
        parameter["teacher_id"] = teacher_id
    if classroom_id != "":
        parameter["classroom_id"] = classroom_id
    
    r = requests.get(url=url, params=parameter)
    print(r.text)

#####################################################################
def change_time(url, lesson_id, new_time):
    # change the time for one lesson
    parameter = {
        "lesson_id": lesson_id,
        "new_time": new_time,
    }
    r = requests.put(url=url, params=parameter)
    print(r.text)

######################################################################
def main():
    # # send event file to micro service
    # creat_time_table('http://127.0.0.1:8000/', 'novy_rozvrh.json')

    # # get the time table with specific teacher, group and classroom
    # group_id = ""
    # teacher_id = ""
    # classroom_id = ""
    # get_time_table('http://127.0.0.1:8000/lessons', group_id, teacher_id, classroom_id)

    # change the time for one lesson
    lesson_id = "01AC6A50-0572-11EC-B041-520D00000000"
    new_time = "8:00 to 9:30, moNday, week 15"
    change_time('http://127.0.0.1:8000/lessons/change_time', lesson_id, new_time)


if __name__ == '__main__':
  main()