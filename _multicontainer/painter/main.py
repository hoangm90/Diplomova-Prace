import aiohttp
import asyncio
import networkx as nx

from fastapi import FastAPI, Request

import planning
           

app = FastAPI()

@app.get('/api/makeplan')
async def compute(request: Request):
    #print("Painter")

    # retrieve input from request body
    input = await request.json()

    subjects = input["subjects"]
    lessons = input["lessons"]
    groups = input["groups"]
    teachers = input["teachers"]
    classrooms = input["classrooms"]
    G = nx.node_link_graph(input["graph"])
    # compute one result
    result = planning.coloring(subjects, lessons, groups, teachers, classrooms, G)
    # return the result
    return result
