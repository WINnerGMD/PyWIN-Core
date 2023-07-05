import hashlib
from fastapi import APIRouter, Request, Form
from fastapi.responses import PlainTextResponse,  HTMLResponse
from database import db
from operator import itemgetter
router = APIRouter(
    prefix="",
    tags=["levels"]
)

def sha1(string):
    sha1 = hashlib.sha1()
    sha1.update(string.encode('utf-8'))
    hashed_string = sha1.hexdigest()
    return hashed_string

def levelHash(data):
    hash = ""
    for x in range(len(data)):
        hash = hash+str(data[x]["levelID"])[0]+str(data[x]["levelID"])[len(str(data[x]["levelID"]))-1]+str(data[x]["stars"])+str(data[x]["coins"])
    return sha1(hash+"xI25fpAapCQg")

@router.post("/winnertests/getGJLevels21.php", response_class=HTMLResponse)
def get_level(str: str = Form(default=""), page: str = Form(), type: str = Form()):
    levelsDataHash = []
    levelString = ""
    userString = ""
    def search_level(result):
        final = []
        for i in result:
            if str in i["levelName"]:
                print("нашел!")
                final.append(i)
        return final
    if type == '2':
        result = db("SELECT * FROM levels")
        result.sort(key=itemgetter('likes'), reverse=True)
    elif type == '1':
        result = db("SELECT * FROM levels")
        result.sort(key=itemgetter('downloads'), reverse=True)
    elif type == '4':
        result = list(reversed(db("SELECT * FROM levels")))
        # if str != "":
        #     result = search_level(answer)
    elif type == '6':
        result =  list(reversed(db("SELECT * FROM levels WHERE `rate` = '1'")))
    elif type == '16':
        result =  list(reversed(db("SELECT * FROM `levels` WHERE `starFeatured` = 1 or `starEpic` = 1;")))
    else:
        result = db("SELECT * FROM levels")
    #     if str != "":
    #         result = search_level(answer)
    print(result)
    for row in result[int(page+"0"):][:10]:
        feature = 0
        epic = 0
        if row['rate'] == 1:
            feature = 1
        elif row['rate'] == 2:
            epic = 1
        levelsDataHash += [{"levelID":row["id"],"stars":row["stars"],"coins":row["coins"]}]

        levelString += f'1:{row["id"]}:2:{row["name"]}:5:{row["version"]}:6:{row["authorID"]}:8:10:9:{row["difficulty"]}0:10:{row["downloads"]}:12:{row["audioTrack"]}:13:{row["gameVersion"]}:14:{row["likes"]}:17:{row["starDemon"]}:43:{row["starDemonDiff"]}:25:{row["starAuto"]}:18:{row["stars"]}:19:{feature}:42:{epic}:45:{row["objects"]}:3:{row["desc"]}:15:{row["levelLength"]}:30:{row["original"]}:31:{row["twoPlayer"]}:37:{row["coins"]}:38:{row["starCoins"]}:39:{row["requestedStars"]}:46:1:47:2:35:{row["songID"]}|'

        userString += f'{row["id"]}:PyWin-bot:{row["id"]}|'
   
    return f"{levelString}#{userString}##{len(result)}:{int(page+'0')}:10#{levelHash(levelsDataHash)}"


@router.post('/winnertests/downloadGJLevel22.php', response_class=PlainTextResponse)
def level_download():
    return "1:62687277:2:test level 5:3:QSB0ZXN0IGxldmVsIGZvciB0aGUgR0QgRG9jcyE=:4:H4sIAAAAAAAAC6WQwQ3DIAxFF3IlfxsIUU6ZIQP8AbJChy_GPSZqpF7-A4yfDOfhXcCiNMIqnVYrgYQl8rDwBTZCVbkQRI3oVHbiDU6F2jMF_lesl4q4kw2PJMbovxLBQxTpM3-I6q0oHmXjzx7N0240cu5w0UBNtESRkble8uSLHjh8nTubmYJZ2MvMrEITEN0gEJMxlLiMZ28frmj:5:1:6:3935672:8:0:9:0:10:1:12:0:13:21:14:0:17::43:0:25::18:0:19:0:42:0:45:1:15:0:30:55610687:31:0:28:1 hour:29:1 hour:35:546561:36::37:0:38:0:39:50:46::47::40::27:AQcHBwEL#1bae6491cc87c72326abcbc0a7afaee139aa7088#f17c5a61f4ba1c7512081132459ddfaaa7c6f716"