from fastapi import FastAPI, WebSocket
import planning

app = FastAPI()

# submit json file
# @app.post("/", tags=["all"])
# def submit_data(data: UploadFile = File(...)):
#     contents = data.file.read()
#     print("ok")
#     return planning.return_planned_timetables(contents)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            raw_data = await websocket.receive_text()
            resp = "hehe ok!"
            await websocket.send_json(resp)
        except Exception as e:
            print(e)
            break