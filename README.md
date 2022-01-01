# Diplomova-Prace
In folder fastapi/helper_function/:
  - File "color_to_time.py": change the color (int) to time (string with hours and date) and change time to color
  - File "coloring.py": from input data, calculating the timetable
  - File "get_data.py": get data from the database (lessons, teachers, groups, classrooms)
  - File "random_sorting.py": random the order of lessons to be planned, but still reserve the order of topics
  - File "sort_lessons.py": input of this file is the lessons from "get_data.py", then the input will be sorted according to the color, and then the result can be returned to users
  - File "submitData.py": input is the json file containing lessons that need to be planned, this file will take the input and add the data to the database for later use
  - File "update_color.py": after using "coloring.py" to chose the colors, times and classrooms, "update_color.py" will update the colors, the times and the chosen classrooms to the database
