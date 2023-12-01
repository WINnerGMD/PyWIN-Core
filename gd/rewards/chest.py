import hashlib

from fastapi import APIRouter, Form, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models

from datetime import datetime
from datetime import timedelta

from config import system
from database import get_db
from utils.crypt import xor_cipher, base64_encode, base64_decode, checkValidGJP
import random

router = APIRouter()


@router.post(f"{system.path}/getGJRewards.php", response_class=PlainTextResponse)
async def chest(
        chk: str = Form(),
        accountID: int = Form(),
        rewardType: int = Form(default=0),
        gjp: str = Form(),
        device: str = Form(..., alias="udid"),
        db: AsyncSession = Depends(get_db)
):
    if await checkValidGJP(accountID, gjp, db):
        resultchk = xor_cipher(base64_decode(chk[5:]), "59182")

        shard_type = random.randint(0, 4)
        shard_count = random.randint(0, 5)
        small_chest_orbs = random.randint(20, 100)
        small_chest_diamonds = random.randint(100, 250)
        big_shest_orbs = random.randint(50, 500)
        big_shest_diamonds = random.randint(500, 1000)

        match rewardType:
            case 1:
                chestmodel = models.ChestsModel(

                    userID=accountID,
                    type=rewardType,
                    orbs=small_chest_orbs,
                    diamonds=small_chest_diamonds,
                    fire_shards=1,
                    ice_shards=1,
                    poison_shards=1,
                    shadow_shards=1,
                    lava_shards=1,
                )
                db.add(chestmodel)

            case 2:
                chestmodel = models.ChestsModel(
                    userID=accountID,
                    type=rewardType,
                    orbs=big_shest_orbs,
                    diamonds=big_shest_diamonds,
                    fire_shards=1,
                    ice_shards=1,
                    poison_shards=1,
                    shadow_shards=1,
                    lava_shards=1,
                )
                db.add(chestmodel)

        small_chest_len = len(
            (await db.execute(select(models.ChestsModel).filter(models.ChestsModel.userID == accountID ).filter(models.ChestsModel.type == 1))).scalars().all())
        big_chest_len = len(
            (await db.execute(select(models.ChestsModel).filter(
                models.ChestsModel.userID == accountID).filter(models.ChestsModel.type == 2))).scalars().all())
        last_big = (await db.execute(select(models.ChestsModel).filter(models.ChestsModel.userID == accountID).filter(
            models.ChestsModel.type == 2 ).order_by(models.ChestsModel.id.desc()))).scalars().first()
        last_small = (await db.execute(select(models.ChestsModel).filter(models.ChestsModel.userID == accountID).filter(
            models.ChestsModel.type == 1).order_by(models.ChestsModel.id.desc()))).scalars().first()

        curent = datetime.now()
        small_chest_sec = timedelta(seconds=15)
        big_chest_sec = timedelta(seconds=15)
        small_time = timedelta()
        big_time = timedelta()




        if last_small != None:
            small_chest_left = curent - last_small.time


            if small_chest_sec < small_chest_left:
                left  = small_chest_left - small_chest_sec
                print(f"nice time left {left.seconds}")
                print(small_chest_sec, small_chest_left)
            else:
                small_time = small_chest_sec - small_chest_left
        if last_big != None:
            big_chest_left = curent - last_big.time
            if big_chest_sec < big_chest_left:
                left = big_chest_left - big_chest_sec
                print(f"nice time left {left.seconds}")
            else:
                big_time = (big_chest_sec - big_chest_left)



        # shards
        shard_first = 0
        shard_second = 0

        shard_count = random.randint(0, 2)

        for index in range(shard_count):
            if index == 0:
                shard_first = random.randint(1, 5)

            elif index == 1:
                shard_second = random.randint(1, 5)
        if shard_first == shard_second:
            print("HUUUUI")
        await db.commit()
        # lam = f"pywin:{accountID}:{resultchk}:{device}:{accountID}:{small_time.seconds}:{small_chest_orbs},{small_chest_diamonds},{shard_first},{shard_second}:{small_chest_len}:{big_time.seconds}:{big_shest_orbs},{big_shest_diamonds},{0},{1}:{big_chest_len}:{rewardType}"
        # lam = f"7Tm2j:{accountID}:{resultchk}:{device}:{accountID}:{small_time.seconds}:{small_chest_orbs},{small_chest_diamonds},1,1:{small_chest_len}:{big_time.seconds}:{big_shest_orbs},{big_shest_diamonds},4,10:{big_chest_len}:{rewardType}"
        lam = f"pywin:{accountID}:{resultchk}:{device}:{accountID}:{small_time.seconds}:{small_chest_orbs},{small_chest_diamonds},{shard_first},{shard_second}:{small_chest_len}:{big_time.seconds}:{big_shest_orbs},{big_shest_diamonds},{shard_first},{shard_second}:{big_chest_len}:{rewardType}"
        encrypt = base64_encode(xor_cipher(lam, "59182"))
        result = (
                "pywin"
                + encrypt
                + "|"
                + hashlib.sha1((encrypt + "pC26fpYaQCtg").encode()).hexdigest()
        )
        print(lam)
        return result


@router.post(f"{system.path}/getGJChallenges.php", response_class=PlainTextResponse)
async def chest(
        chk: str = Form(),
        accountID: str = Form(),
        gjp: str = Form(),
        device_id: str = Form(..., alias="udid"),
):
    resultchk = xor_cipher(base64_decode(chk[5:]), "19847")

    lam = f"dQbAT:{accountID}:{resultchk}:{device_id}:{accountID}:8203:1,2,2,5,Coin Finder:1,3,10,10,Star Collector:1,1,1000,15,Orb Master"
    encrypt = base64_encode(xor_cipher(lam, "19847"))
    result = (
            "hUiNy"
            + encrypt
            + "|"
            + hashlib.sha1((encrypt + "oC36fpYaPtdg").encode()).hexdigest()
    )
    print(result)
    return result
