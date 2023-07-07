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


def downloadLevelHash1(levelString):
    hash = ""
    dataLen = len(levelString)
    divided = int(dataLen/40)
    p = 0
    k = 0
    while k < dataLen:
        if p > 39: break
        hash += levelString[k]
        p+=1
        k = k + divided
    return sha1(hash+"xI25fpAapCQg")

def downloadLevelHash2(levelData):
    return sha1(levelData+"xI25fpAapCQg")

@router.post('/winnertests/downloadGJLevel22.php', response_class=PlainTextResponse)
def level_download(levelID: str = Form()):
    levelString = "H4sIAAAAAAAAC6WXUZLkIAiGL5StEgWV2qc5wxzAA8wV9vDbielEvumprtp9if3_AiIi0l-fpW8yNI08JNsoI5sNkTnkOUyyDkkpjTZkiO2fPtLoQ_7IOLRTfqst_6qt45dME_7SxC4zFd65kMeu-n829KX-Hr6nfnq3DfvRjfTeidtM_cHM9vUhZUv7YHOoc9Dt8Z2_22TOoe_DZ_ED5eM7DRwTH3p856ykOciWfssmW95yt61sYicsEqEGqCXCGqEHaPmCfYcWZ3uYrRJhXLe2AFuKMHrVbq8eE3nrhx_5CV0C3A804Iz5gnm9zdUdW4yYtBhQ6ZjvcWvZDRgHknAiSYEbDjABF-AaIl3EI84ZOPpXmDDMmCVlDn3FestJHwEt8_jyU79jvY71HOs51vMWsKYEjBxOS7r4QRwBqReWDGxPfOhL9E8L7BdckhJviWqMt6oBx4uiJsC4ohbzQWsChn8d8XLEywswLz1ufcrAuPcpxstEgBU4-mfFgGN8zCrw4l_ZiXYs-FhlL7NXNTq0NFkkSiOhJATE436AMBL5JhC8iRX4cqLi8td5-RX4drLOanAbOKtBuokZrnITTiLFfZ7Evc_T6HfCsMpKOIiz7BQQq4S9JJa9nKWJxOLYWawSiGVzs3ytRHspsdpoIOYzuagoQ6j1pcQ3GytRSTg2pzw5YwiNIZyv8ErwGM5nu0BlIWZBX2ycFX6RUEooJRolGiTmm79INOZYY46dbUKBykow-RvTsjGmnTHtjGlnCPsawryI-N3QxKLaUqwLTTKwAcei2rIAKzAaqsKOKhb9VipwbBqawj-Ffwr_0DQ1PGLNYtFvNQGz5UP8KuLX4J9jvw57jv163G_HI9fxyPXlkTt70NhF9hKb0q4a8XzFblx7xB32HE1uuuzt_jiaOEcT52jiHH2_l5gvrgk45ouj6XON8XOL8XP8OXCDfxX-4f-B15gv3hIw_GsxX7zFfPEO_66m9C_bF5V-dQ8AAA=="

    row = db(f"SELECT * FROM levels WHERE id = {levelID}")[0]
    print(row)
    return f'1:{row["id"]}:2:{row["name"]}:3:{row["desc"]}:4:{levelString}:5:{row["version"]}:8:10:9:{row["difficulty"]}:10:{row["downloads"]}:12:{row["audioTrack"]}:13:{row["gameVersion"]}:14:{row["likes"]}:17:{row["starDemon"]}:43:{row["starDemonDiff"]}:25:{row["starAuto"]}:18:{row["stars"]}:19:{"1" if row["rate"] == 1 else "0"}:42:{"1" if row["rate"] == 2 else "0"}:45:{row["objects"]}:15:{row["levelLength"]}:30:{row["objects"]}:31:{row["twoPlayer"]}:28:{row["uploadDate"]}:29:{row["updateDate"]}:35:{row["songID"]}:36::37:{row["coins"]}:38:{row["starCoins"]}:39:{row["requestedStars"]}:46::47::40:{row["isLDM"]}:27:Aw==#{downloadLevelHash1(levelString)}#' + downloadLevelHash2(f"{str(row['authorID'])},{str(row['stars'])},{str(row['starDemon'])},{str(row['id'])},{str(row['starCoins'])},{'1' if row['rate'] == 1 else '0'},{str(row['password'])},0")