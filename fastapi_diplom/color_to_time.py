def color_to_time(num_color: int):
    hour = ["8:00 to 9:30", "9:50 to 11:20", "11:40 to 13:10", "14:30 to 16:00", "16:20 to 17:50"]
    day_in_week = ["Monday", "Tueasday", "Wednesday", "Thursday", "Friday"]
    color_time = []
    for i in range(num_color):
        time_string = hour[i%5] + ", " + day_in_week[(int(i/5))%5] + ", week " + str(int(i/25)+1)
        color_time.append(time_string)
    return color_time