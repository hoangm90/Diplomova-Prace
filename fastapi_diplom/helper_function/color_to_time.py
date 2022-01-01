def color_to_time(num_color: int):
    hour = ["8:00 to 9:30", "9:50 to 11:20", "11:40 to 13:10", "14:30 to 16:00", "16:20 to 17:50"]
    day_in_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    color_time = []
    for i in range(num_color):
        time_string = hour[i%5] + ", " + day_in_week[(int(i/5))%5] + ", week " + str(int(i/25)+1)
        color_time.append(time_string)
    return color_time

def time_to_color(new_time: str):
    time_array = new_time.split()
    hour = {"8:00 to 9:30,": 0, "9:50 to 11:20,": 1, "11:40 to 13:10,": 2, "14:30 to 16:00,": 3, "16:20 to 17:50,": 4}
    day_in_week = {"Monday,": 0, "Tuesday,": 1, "Wednesday,": 2, "Thursday,": 3, "Friday,": 4}
    if len(time_array) != 6:
        return -1
    try:
        week = int(time_array[5])
    except ValueError:
        return -1
    
    new_hour = time_array[0] + " " + time_array[1] + " " + time_array[2]
    if hour.get(new_hour) == None or day_in_week.get(time_array[3]) == None:
        return -1
     
    color = hour[new_hour] + day_in_week[time_array[3]]*5 + (week-1)*25
    return color
