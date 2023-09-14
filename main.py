import logging as log
import aiohttp
import asyncio
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from timetable_parser import Parser

app = FastAPI()

templates = Jinja2Templates(directory="templates")

log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Create client session instance
session = aiohttp.ClientSession()

load_dotenv()

# Create parser instance
parser = Parser(
    os.getenv('URL'),
    os.getenv('GROUP_ID'),
    os.getenv('LOGIN'),
    os.getenv('HASHED_PASSWORD'),
    session
)

asyncio.create_task(parser.login())


@app.get("/json")
async def json():
    return await parser.getTimetable('2023-09-11', '2023-09-24')


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    table = list(filter(lambda x: x is not None, map(formatDay, await parser.getTimetable('2023-09-11', '2023-09-24'))))

    print(table)

    return templates.TemplateResponse('index.html', {
        'request': request,
        'timetable': table,
    })

def formatDay(day: dict):
    if len(day['lessons']) == 0:
        return None
    
    day['date'] = day['date'][5:10]
    day['lessons'] = list(filter(lambda x: x is not None, map(formatLesson, day['lessons'])))

    return day


def formatLesson(lesson: dict):
    if 'name' not in lesson:
        return None

    return {
        'time': f'{lesson["startTime"]}-{lesson["endTime"]}',
        'name': lesson['name'],
        'cabinet': lesson['timetable']['classroom']['name']
    }
