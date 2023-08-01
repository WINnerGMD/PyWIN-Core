from plugins.origins import PyWIN
from fastapi import Form, Request
from database import db
from operator import itemgetter
import hashlib
from fastapi.responses import PlainTextResponse
import base64
import requests
app = PyWIN(name="1 point 9", token="nil")


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


@app.router.post('/winnertests/getGJLevels19.php', response_class=PlainTextResponse)
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
    for row in result[int(page+"0"):][:10]:
            feature = 0
            epic = 0
            if row['rate'] == 1:
                feature = 1
            elif row['rate'] == 2:
                epic = 1

            levelsDataHash += [{"levelID":row["id"],"stars":row["stars"],"coins":row["coins"]}]
            levelString += f'1:{row["id"]}:2:{row["name"]}:5:{row["version"]}:6:{row["authorID"]}:8:10:9:{row["difficulty"]}0:10:{row["downloads"]}:12:{row["audioTrack"]}:13:{row["gameVersion"]}:14:{row["likes"]}:17:{row["starDemon"]}:43:{row["starDemonDiff"]}:25:{row["starAuto"]}:18:{row["stars"]}:19:{feature}:42:{epic}:45:{row["objects"]}:3:{row["desc"]}:15:{row["levelLength"]}:30:{row["original"]}:31:{row["twoPlayer"]}:37:{row["coins"]}:38:{row["starCoins"]}:39:{row["requestedStars"]}:46:1:47:2:35:{row["songID"]}|'

            userString += f'{row["authorID"]}:pywin:{row["authorID"]}|'
    
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

def base64_encode(string):
    return base64.b64encode(str(string).encode("utf-8")).decode("utf-8")

def xor_cipher(text, key):
    # потом перепишу с php на py
    return requests.get(f"https://xor-cipher.dimluxdev.repl.co/?text={text}&key={key}").text

@app.router.post(f'/winnertests/downloadGJLevel19.php', response_class=PlainTextResponse)
def level_download(levelID: str = Form()):
    # levelString = "H4sIAAAAAAAAC6WX0ZHdIAxFG3JmAEmAJ19bwxZAAdtCis_DkEl2pEM2kx_zfIwvAmR038e79CsPTaOMXGzIKGYj59WU1Syo41sedeSU0mgjj2zz0kcafeQfeTwSqXxNIv-_xB1KzD7rhS-JlDHfj4TmavwSSn-TMZRJ_xJNBZnr4y3LlWZjq6mr0et1Xb_bIrvps3mX-7krz3UJPA_e9LmupzmtJl_pe77yVa5ml1yvyK7yuk9JN9YY5xg_IpJDXHqs7XCO8SOS71AEcClxJMU-DeV6ZdnT-3zv-1Xg95H71azAE_BHRzTWCbgcuduvNS7xYMcEeAV-n3gw7sPnKJH-vEbxBDwduUuiPV_Y96D_DVyO_V08c8Ro3JkJIe_AS5w_W8fzfuLSYh3kLt9WPMR9Puz-Lh-2vuf9xOduRjoBL0fu8nBzt79b3_MOvEA-2JH7ePqRe50O628xFzg3BU5dgXIhUF0EitHiPt-WTsDzkbs82TqeQ12TBvOFWiVQrFY8AX90YLowK49bvOmbuyTZQRJ3H8UO3vMGXCGefOQ-HnAVArZCwFfszXWHkkLxVQEORVyh6C-ubn2WTsAFeDpxn_wKxV3BDKx4Ag7FWsGcKBRTBXOlUDQViq9C8VUwD1uHOKx_wNOJw_L7NFfwLAoeZ-v48AU4eA0Fj6bg6RQ84N52P98KXI7pCelD20vx-LQy8EQGnsjAExl4IgNPtMYl7j9fA69k4K12PMTdZ2rgoQw8l4HHMfA4Bp7FwOMYeCsDz2vgeQ28pIH3scBrd_n9QqIH4h8EduzPB4EUGM0KhqmCYapgmCrUtqUT8HzkLikq1OAKNbiCwapg1CrU7ApeoYLBqmDIamDgno2p20t9vvcb1cAkNDAJDUxCg1O4wenWoPg2KNYNinsDM9DgFG5gKhqc5g2qRYPq0uHr7fBPpMM_l9slzk8cFHWi9RQAAA=="

    row = db(f"SELECT * FROM levels WHERE id = {levelID}")[0]
    
    return f'1:{row["id"]}:2:{row["name"]}:3:{row["desc"]}:4:{row["string"]}:5:{row["version"]}:6:{row["authorID"]}:8:10:9:{row["difficulty"]}0:10:{row["downloads"]}:12:{row["audioTrack"]}:13:{row["gameVersion"]}:14:{row["likes"]}:17:{row["starDemon"]}:43:{row["starDemonDiff"]}:25:{row["starAuto"]}:18:{row["stars"]}:19:{"1" if row["rate"] == 1 else "0"}:42:{"1" if row["rate"] == 2 else "0"}:45:{row["objects"]}:15:{row["levelLength"]}:30:{row["original"]}:31:{row["twoPlayer"]}:28:{row["uploadDate"]}:29:{row["updateDate"]}:35:{row["songID"]}:36::37:{row["coins"]}:38:{row["starCoins"]}:39:{row["requestedStars"]}:46::47::40:{row["isLDM"]}:27:{base64_encode(xor_cipher(row["password"], 26364))}#{downloadLevelHash1(row["string"])}#' + downloadLevelHash2(f'{row["authorID"]},{row["stars"]},{row["starDemon"]},{row["id"]},{row["starCoins"]},{"1" if row["rate"] == 1 else "0"},{row["password"]},0')




@app.router.post(f'/winnertests/uploadGJLevel19.php')
def upload_level(levelString: str = Form(),
                  accountID: str = Form(),
                    levelName: str = Form(),
                    #  levelDesc: str = Form(),
                      levelVersion: str = Form(), 
                      levelLength: str = Form(),
                        audioTrack: str = Form(),
                        password: str = Form(),
                            original: str = Form(),
                            twoPlayer: str = Form(),
                            songID: str = Form(),
                            objects: str = Form(),
                            gameVersion: str = Form()
                            ):
    if int(objects) > 100:
        db(f"INSERT INTO `levels`(`name`,`version`, `authorID`, `gameVersion`, `audioTrack`, `levelLength`, `coins`, `original`, `twoPlayer`, `songID`, `requestedStars`, `isLDM`, `objects`, `password`, `uploadDate`, `updateDate`, `string`) VALUES ('{levelName}','{levelVersion}','{accountID}','{gameVersion}','{audioTrack}','{levelLength}','0','{original}','{twoPlayer}','{songID}','0','0','{objects}','{password}','111','111','{levelString}')")
    # return db(f"SELECT * FROM `levels` WHERE `name` = '{levelName}' and `authorID` = '{accountID}'")[0]["id"]
    return "1"