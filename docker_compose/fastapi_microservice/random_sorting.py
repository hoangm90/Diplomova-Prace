import time, random

def sort_helper(e):
    num = 0
    i = 0
    while e[i] >= "0" and e[i] <= "9":
        num = num*10 + int(e[i])
        i+=1
    return num

def random_sorting(subjects):
    ls = []
    ls.append([])
    for lesson in subjects["no_subject"]:
        ls[0].append(lesson)
    t = 1000 * time.time() # current time in milliseconds
    random.seed(int(t) % 2**32)
    random.shuffle(ls[0])
    i=1
    for sub in subjects:
        if sub == "no_subject":
            continue
        else:
            ls.append([])
            topic_list = []
            for topic in subjects[sub]:
                topic_list.append(topic)
            topic_list.sort(reverse=True, key=sort_helper)
      
            for tp in topic_list:
                ls1 = []
                for lesson in subjects[sub][tp]:
                    ls1.append(lesson)
                random.shuffle(ls1)
                for lesson in ls1:
                    ls[i].append(lesson)
            i += 1

    dict_previous = {}
    for i in range(len(ls)):
        for j in range(len(ls[i])-1):
            dict_previous[ls[i][j]] = ls[i][j+1]
        dict_previous[ls[i][len(ls[i])-1]] = 0

    ls2 = []
    for i in range(len(ls)):
        for j in range(len(ls[i])):
            ls2.append(i)
    random.shuffle(ls2)
  
    ls3 = []
    for i in ls2:
        ls3.append(ls[i].pop())
    return ls3, dict_previous