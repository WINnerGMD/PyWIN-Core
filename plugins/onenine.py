from plugins.origins import PyWIN
from fastapi import Request, Form, Depends
from fastapi.responses import PlainTextResponse
from services.levels import LevelService
from objects.levelObject import LevelGroup, LevelObject
from config import system
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from objects.schemas import GetLevel, UploadLevel, UploadComments
from logger import *
from utils.gdform import gd_dict_str
from helpers.rate import Difficulty
from utils.crypt import sha1_hash
from services.comments import CommentsService
from services.user import UserService
from services.leader_boards import LeaderBoardsService

app = PyWIN("onenine")


async def GDGet_level(service, page: int | None = 0, is_gauntlet: bool = False):
    levelsDataHash = ""
    levelData = []
    userString = ""
    for row in service["database"]:
        feature = 0
        epic = 0
        if row.rate == 1:
            feature = 1
        elif row.rate == 2:
            epic = 1

        levelsDataHash += str(row.id)[0] + str(row.id)[-1] + str(row.stars)

        Level = gd_dict_str(
            {
                1: row.id,
                2: row.name,
                3: row.desc,
                5: row.version,
                6: row.authorID,
                8: 10,
                9: row.difficulty * 10 if row.difficulty != -3 else 0,
                10: row.downloads,
                12: row.AudioTrack,
                13: row.gameVersion,
                14: row.likes,
                15: row.lenght,
                17: 0,
                18: row.stars,
                19: feature,
                25: 1 if row.difficulty == -3 else 0,
                30: row.original,
                31: row.two_players,
                35: row.song_id,
            }
        )

        levelData.append(Level)
        # levelString += f'1:{row.id}:2:{row.name}:5:{row.version}:6:{row.authorID}:8:10:9:{row.difficulty}0:10:{row.downloads}:12:{row.AudioTrack}:13:{row.gameVersion}:14:{row.likes}:17:{0}:43:{0}:25:{0}:18:{row.stars}:19:{feature}:42:{epic}:45:{row.objects}:3:{row.desc}:15:{row.lenght}:30:{row.original}:31:{row.two_players}:37:{row.coins}:38:{row.user_coins}:39:{0}:46:1:47:2:35:{row.song_id}|'

        userString = f"{row.authorID}:{row.authorName}:{row.authorID}|"
    levelstr = "|".join(levelData)
    return f"{levelstr}#{userString}##{service['count']}:{page * 10}:10#"
    # return "1:5085:2:HI:5:1:6:2204:8:10:9:30:10:9483:12:0:13:1:14:562:3:aGk=:15:3:17:1:18:10:19:1:25:0:30:0:31:0:35:0|1:7707:2:On My Way:5:1:6:3527:8:10:9:20:10:6052:12:1:13:1:14:506:3:QmFjayBPbiBUcmFjayBpbiBQcmFjdGljZSBNb2RlLiBFbmpveSE=:15:3:17:0:18:3:19:0:25:0:30:0:31:0:35:0|1:7660:2:Time Machine:5:1:6:6531:8:10:9:50:10:5470:12:7:13:1:14:470:3: :15:3:17:0:18:0:19:0:25:0:30:0:31:0:35:0|1:4:2:Zimnior:5:2:6:2:8:10:9:30:10:17084:12:6:13:1:14:437:3:Wg==:15:2:17:0:18:5:19:1:25:0:30:0:31:0:35:0|1:2085:2:Extreme Park:5:1:6:388:8:10:9:50:10:4677:12:6:13:3:14:404:3:VGhpcyBpcyBleHRyZW1lbHkgaGFyZCBsZXZlbC4gUHJhY3RpY2UgbWFrZXMgcGVyZmVjdCEhISBOZXh0IHRpbWUgSSB3aWxsIG1ha2UgZWFzaWVyIGxldmVsLg==:15:3:17:1:18:10:19:1:25:0:30:56287:31:0:35:0|1:7913:2:Insomniac:5:1:6:6733:8:10:9:50:10:4068:12:9:13:4:14:381:3:Y29vbCBsZXZlbA==:15:2:17:1:18:10:19:1:25:0:30:0:31:0:35:0|1:4446:2:double time:5:1:6:2293:8:10:9:20:10:14098:12:4:13:1:14:374:3: :15:2:17:0:18:3:19:1:25:0:30:0:31:0:35:0|1:291:2:Bright side of life:5:1:6:138:8:10:9:50:10:18477:12:4:13:1:14:364:3:SSBuYW1lZCB0aGlzIGxldmVsIGFmdGVyIG9uZSBvZiBteSBmYXZvcml0ZSBzb25ncyAtIEFsd2F5cyBsb29rIG9uIHRoZSBicmlnaHQgc2lkZSBvZiBsaWZlLiBJZGsgd2h5LCBidXQgd2h5IG5vdCB4ZA==:15:3:17:1:18:10:19:1:25:0:30:0:31:0:35:0|1:10679:2:the imposible level:5:1:6:8549:8:10:9:50:10:4052:12:0:13:5:14:351:3: :15:2:17:1:18:10:19:1:25:0:30:0:31:0:35:0|1:10451:2:iIiDeMasteriIi:5:1:6:8289:8:10:9:30:10:3281:12:4:13:4:14:342:3: :15:2:17:0:18:5:19:1:25:0:30:0:31:0:35:0#2204:FG:0|3527:Benedict:0|6531:Semoleg:0|2:warlom:0|388:Player:0|6733:Insomneux:0|2293:2013:0|138:Sunrise:0|8549:swamp:0|8289:a1tr1st1:0##29851:10:10#"


@app.router.post(f"{system.path}/getGJLevels19.php", response_class=PlainTextResponse, tags=['1.9'])
async def get_level(
    request: Request,
    str: str = Form(default=None),
    page: int = Form(default=None),
    type: int = Form(default=None),
    len: int | str = Form(default=None),
    accountID: int = Form(default=None),
    diff: int | str = Form(default=None),
    demonFilter: int = Form(default=None),
    featured: str = Form(default=None),
    epic: str = Form(default=None),
    coins: str = Form(default=None),
    song: str = Form(default=None),
    gauntlet: int = Form(default=None),
    customSong: str = Form(default=None),
    db: AsyncSession = Depends(get_db),
):
    if str is not None:
        if "," in str:
            result = await LevelService.get_levels_group(db=db, levels=str.split(","))
            is_gauntlet = False
            page = 0

    if diff not in ["-", None]:
        difficulty = Difficulty(int(diff))
    else:
        difficulty = None
    scheme = GetLevel(
        lenght=len if len != "-" else None,
        string=str,
        searchType=type,
        accountID=accountID,
        difficulty=difficulty,
        demonFilter=demonFilter,
        page=page,
        featured=featured,
        epic=epic,
        coins=coins,
        song=song,
        customSong=customSong,
        gauntlet=gauntlet,
    )
    info(scheme)
    result = await LevelService().test_get_levels(db=db, data=scheme)
    info(result)
    page = page
    is_gauntlet = False
    if result["status"] == "ok":
        level = await GDGet_level(service=result, page=page, is_gauntlet=is_gauntlet)
        return level
    else:
        error(result["details"])
        return


@app.router.post(f"{system.path}/downloadGJLevel19.php", response_class=PlainTextResponse, tags=['1.9'])
async def level_download(levelID: str = Form(), db: AsyncSession = Depends(get_db)):
    if int(levelID) < 0:  # daily & weekly
        service = await LevelService().get_level_buid(db=db, levelID=8)
        is_featured = True
    else:
        service = await LevelService().get_level_buid(db=db, levelID=levelID)
        is_featured = False
    return await LevelObject(service=service, db=db).GDDownload_level(
        is_featured=is_featured
    )


@app.router.post(f"{system.path}/updateGJUserScore19.php", response_class=PlainTextResponse, tags=['1.9'])
async def clen():
    return "1"


@app.router.post(f"{system.path}/getGJScores19.php", response_class=PlainTextResponse, tags=['1.9'])
async def getScores(db: AsyncSession = Depends(get_db)):
    result = await LeaderBoardsService().leaderboard(db=db)
    count = 1
    string = ""
    for i in result:
        iconkit = i.iconkits

        string += f"1:{i.userName}:2:{i.id}:3:{i.stars}:4:{i.demons}:6:{count}:7:{i.id}:8:{i.cp}:9:{iconkit['accIcon']}:10:{iconkit['color1']}:11:{iconkit['color2']}:13:{i.coins}:14:0:15:{i.id}:16:{i.id}:17:{i.usr_coins}:46:{i.diamonds}|"
        count += 1
    return string[:-1]


@app.router.post(f"{system.path}/uploadGJLevel19.php", tags=['1.9'])
async def upload_level(
    db: AsyncSession = Depends(get_db),
    levelString: str = Form(),
    accountID: str = Form(),
    levelName: str = Form(),
    levelDesc: str = Form(default="[Hey he didn't put a description]"),
    levelVersion: str = Form(),
    levelLength: str = Form(),
    audioTrack: str = Form(),
    password: str = Form(),
    twoPlayer: str = Form(),
    songID: str = Form(),
    objects: str = Form(),
    gameVersion: str = Form(),
):
    SystemObj = UploadLevel(
        levelString=levelString,
        accountID=accountID,
        levelName=levelName,
        levelDesc=levelDesc,
        levelVersion=levelVersion,
        levelLength=levelLength,
        audioTrack=audioTrack,
        password=password,
        original=0,
        twoPlayer=twoPlayer,
        songID=songID,
        objects=objects,
        coins=0,
        requestedStars=0,
        ldm=0,
        gameVersion=gameVersion,
    )
    return (await LevelService().upload_level(db=db, data=SystemObj)).id


@app.router.post(f"{system.path}/uploadGJComment19.php", response_class=PlainTextResponse, tags=['1.9'])
async def upload_comment(
    accountID: str = Form(default=None),
    userName: str = Form(default=None),
    comment: str = Form(default=None),
    levelID: str = Form(default=None),
    percent: str = Form(default=None),
    db: AsyncSession = Depends(get_db),
):
    comment_object = UploadComments(
        userName=userName,
        accountID=accountID,
        comment=comment,
        levelID=levelID,
        percent=percent,
    )
    answer = await CommentsService().upload_comments(db=db, data=comment_object)
    if answer["status"] == "ok":
        if answer["type"] == "comment":
            return str(answer["data"].id)
    else:
        error(answer["details"])
    # return "2~ODk4IHRvIGp1c3QgYmVhdCBpbiBwcmFjdGlzZSBtb2RlIGdnIQ==~3~133533914~4~9~7~2~10~1~9~2 minutes~6~31468976:1~depolo~9~41~10~25~11~10~14~~15~1~16~13735168#5705:0:10"


@app.router.post(f"{system.path}/getGJComments19.php", response_class=PlainTextResponse, tags=['1.9'])
async def get_user(
    db: AsyncSession = Depends(get_db), levelID: str = Form(), page: str = Form()
):
    comments_object = (await CommentsService().get_comments(db=db, level_id=levelID))[
        "database"
    ]
    comment_string = ""
    user_string = ""
    for i in comments_object:
        userObject = (await UserService().get_user_byid(db=db, id=i.authorId))[
            "database"
        ]
        iconkits = userObject.iconkits
        comment_string += f"2~{i.content}~3~{i.authorId}~4~{i.likes}~7~{i.is_spam}~10~{i.progress}~9~2 minutes~6~31468976~9~{iconkits['accIcon']}~10~{iconkits['color1']}~11~{iconkits['color2']}~14~0~15~0~16~{i.authorId}|"
        user_string = f"{i.authorId}:{i.authorName}:{i.authorId}|"
    return comment_string + "#" + user_string + "#5705:2:10"
    # return str(comments_object)
