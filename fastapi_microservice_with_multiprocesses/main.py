import json, copy
from fastapi import FastAPI, WebSocket
import multiprocessing

import planning, divide_data, assemble_data

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            lessons_raw = data["events"]
            
            # divide raw lessons into two set
            les1, les_raw1, les2, les_raw2 = divide_data.divide_data(lessons_raw)
    
            data1 = copy.deepcopy(data)
            data1["events"] = les_raw1
            data2 = copy.deepcopy(data)
            data2["events"] = les_raw2

            queue1 = multiprocessing.Queue() 
            queue2 = multiprocessing.Queue()

            # create processes 
            p1 = multiprocessing.Process(target=planning.return_planned_timetables, args=(data1, les1, queue1))
            p2 = multiprocessing.Process(target=planning.return_planned_timetables, args=(data2, les2, queue2))
            
            # start processes
            p1.start()
            p2.start()

            # need to queue.get before join or it will cause deadlock
            arr1 = queue1.get()
            arr2 = queue2.get()

            # wait until processes end before doing next instructions
            p1.join()
            p2.join()
            
            # assemble lessons
            resp = assemble_data.assemble_lessons(arr1, arr2, data)
            
            # send the result to client
            await websocket.send_json(resp)
        except Exception as e:
            print(e)
            break