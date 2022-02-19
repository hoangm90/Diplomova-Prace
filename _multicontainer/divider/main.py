import aiohttp
import asyncio
import json
from fastapi import FastAPI, Request, WebSocket
import divide_data, assemble_data
           

serverUrl = 'comparer'

app = FastAPI()

@app.get('/api/makeplan')
async def compute(request: Request):
    
    # this retrieve JSON structure from request body
    input = await request.json()

    # now divide the input into parts (two in this case)
    inputs = divide_data.divide_data(input)

    async def fetch(input):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{serverUrl}:8000/api/makeplan/', json=input) as resp:
                return await resp.json() 

    # ask services for a solution
    queries = [fetch(input) for input in inputs]
    # jsons is list which contains a subsolutions
    jsons = await asyncio.gather(*queries)
    
    # join the subsolutions
    result = assemble_data.assemble_lessons(jsons[0], jsons[1])
    # return results
    return result

@app.websocket('/api/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            raw_input = await websocket.receive_text()
            input = json.loads(raw_input)
            
            # now divide the input into parts (two in this case)
            inputs = divide_data.divide_data(input)

            async def fetch(input):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'http://{serverUrl}:8000/api/makeplan/', json=input) as resp:
                        return await resp.json() 

            # ask services for a solution
            queries = [fetch(input) for input in inputs]

            # jsons is list which contains a subsolutions
            jsons = await asyncio.gather(*queries)
            # join the subsolutions
            print("ok")
            result = assemble_data.assemble_lessons(jsons[0], jsons[1])
            # return results
            await websocket.send_json(result)
        except Exception as e:
            print(e)
            break
