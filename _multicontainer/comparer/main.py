import aiohttp
import asyncio

from fastapi import FastAPI, Request
import provide_needed_input, add_color_to_lecture       

serverUrl = 'painter'

app = FastAPI()

@app.get('/api/makeplan')
async def compute(request: Request = None):
    # this is API endpoint, it is expected to run 10 experiments
    input = await request.json()
    return await getResults(10, input)

@app.get('/api/makeplan/{count}')
async def compute(count: int = 10, request: Request = None):
    # this is API endpoint, it is expected to run count experiments
    input = await request.json()
    return await getResults(count, input)

async def getResults(count, input):
    needed_input = provide_needed_input.return_needed_input(input)

    async def fetch():
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{serverUrl}:8000/api/makeplan/', json=needed_input) as resp:
                return await resp.json() 

    # ask count times for solutions
    queries = [fetch() for index in range(count)]
    # retrieve JSONs
    jsons = await asyncio.gather(*queries)

    # pick up the best solution from given
    best_colors = None
    chosen_classrooms = None
    best_max_colors = -1
    for item in jsons:
        colors = item['colors']
        max_color = item['max_color']

        if best_max_colors == -1:
            best_max_colors = max_color
            best_colors = colors
            chosen_classrooms = item["chosen_classrooms"]
        elif max_color < best_max_colors:
            best_max_colors = max_color
            best_colors = colors
            chosen_classrooms = item["chosen_classrooms"]
    
    bestResult = add_color_to_lecture.return_planned_timetables(input, best_colors, chosen_classrooms, best_max_colors)

    # return the best result
    return bestResult
