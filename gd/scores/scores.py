from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from config import path
from database import db
from operator import itemgetter
import json

router = APIRouter()

@router.post(f"{path}/getGJScores20.php", response_class=PlainTextResponse)
def getScores():
    result = db("SELECT * FROM `users` WHERE `verifed` = 1;")
    result.sort(key=itemgetter('stars'), reverse=True)

    string = ""
    count = 1
    for i in result:

        iconkit = json.loads(i['iconkit'])

        string += f"1:{i['userName']}:2:{i['id']}:13:{i['coins']}:17:{i['usr_coins']}:6:{count}:9:{iconkit['accIcon']}:10:{iconkit['color1']}:11:{iconkit['color2']}:14:0:15:2:16:{i['id']}:3:{i['stars']}:8:0:46:{i['diamonds']}:4:{i['demons']}|"
        count += 1
    return string[:-1]

@router.get(f"{path}/getGJScores20.php", response_class=PlainTextResponse)
def get():
    result = db("SELECT * FROM `users` WHERE `verifed` = 1;")
    result.sort(key=itemgetter('stars'), reverse=True)
    answer = []

    for i in result:
        answer.append({"name": i['userName'], "id": i['id'], "role": i['role'], "stars": i['stars'], "diamonds": i['diamonds']})

    return str(result)

    