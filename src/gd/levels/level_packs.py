from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import system
from src.models import GauntletsModel
from src.services.levels import LevelService
from src.utils.gdform import gd_dict_str
from src.utils.crypt import return_hash
from src.depends.gauntlets import GauntletsRepository
import numpy

router = APIRouter(tags=["Packs"], default_response_class=PlainTextResponse)

@router.post(f"{system.path}/getGJGauntlets21.php")
async def gauntlets():
    gauntlets = await GauntletsRepository().find_all()
    response = ""
    hash_string = ""
    for gn in numpy.arange(gauntlets):
        single_response = {1: gn.indexpack, 3: gn.levels}

        hash_string += f"{gn.indexpack}{gn.levels}"
        response += gd_dict_str(single_response) + "|"

    response = response[:-1] + f"#{return_hash(hash_string, 'xI25fpAapCQg')}"
    print(response)
    return response


@router.post(f"{system.path}/getGJMapPacks21.php")
async def map_packs(page: str = Form()):
    packs = await LevelService.get_map_packs(db=db, page=int(page))
    packstrings = []
    packhash = ""
    for pack in packs["database"]:
        packstrings.append(
            gd_dict_str(
                {
                    1: pack.id,
                    2: pack.name,
                    3: pack.levels,
                    4: pack.stars,
                    5: pack.coins,
                    6: pack.difficulty,
                    7: pack.text_color,
                    8: pack.bar_color,
                }
            )
        )
        packhash += f"{str(pack.id)[0]}{str(pack.id)[-1]}{pack.stars}{pack.coins}"
    return (
        "|".join(packstrings)
        + f"#{packs['count']}:{int(page) * 10}:10#"
        + return_hash(packhash, 'xI25fpAapCQg')
    )



@router.post(f"{system.path}/getGJLevelLists.php")
async def lists(req: Request):
    print(await req.form())
    return """1:50:2:Memory Lane:3::5:5:49:2795:50:ViPriN:10:1123576:7:6:14:30225:19:1:51:2915652,10541049,11849346,17235008,15619194,2997354,8660411,49941534,5433594,4284013:55:60:56:7:28:17030
36777:29:1|1:822:2:The Thes:3:QWxsIGxldmVscyBpbiB0aGUgJ1RoZScgc2VyaWVzLg==:5:1:49:1275405:50:Subwoofer:10:257672:7:3:14:16513:19:1:51:65707442,65726952,70111986,70182441:55:20:56:3
:28:1703039713:29:0|1:4788:2:Progression Level 1:3:R0QgQmVnaW5uZXJzIExpc3QgbGV2ZWwgMSEgR29vZCBsaXN0IG9mIGxldmVscyB0byBpbnRyb2R1Y2UgZnJpZW5kcyB0byB0aGUgZ2FtZSE=:5:5:49:6061424:50:tr
icipital:10:222788:7:1:14:12600:19:1:51:90752263,59760047,88982532,78743788,88022936,89413344,90994090,74542823,74612523,55037478:55:20:56:5:28:1703050435:29:1703402400|1:101:2:my 
least favorite levels:3::5:1:49:12308929:50:BLEACHwav:10:143811:7:10:14:9547:19::51:6508283:55:0:56:0:28:1703037187:29:0|1:811:2:Fun Factory:3:QSBjb2xsZWN0aW9uIG9mIHNvbWUgb2YgbXkgZ
mF2b3JpdGUgZmFjdG9yeSBsZXZlbHMh:5:1:49:1275405:50:Subwoofer:10:447049:7:4:14:9290:19:1:51:79445419,78237459,48297506,96611738,93358704,90459731,57368204:55:20:56:5:28:1703039688:29
:0|1:29:2:Snowy Season:3:QSBjb2xsZWN0aW9uIG9mIHdpbnRlci10aGVtZWQgbGV2ZWxzIGZvciB0aGUgY29sZCBzZWFzb24uIEhhcHB5IEhvbGlkYXlzISA6KQ==:5:1:49:1093804:50:AutoNick:10:394533:7:4:14:8746:1
9:1:51:67180546,66345531,90475659,75452865,66008410,76828348,66001175,66010605,51797882,77617824,77399845,85928041,58865383,87108496,79106348:55:30:56:6:28:1703035938:29:0|1:28:2:M
y Verifications:3:TGV2ZWxzIEkgdmVyaWZpZWQhISE=:5:1:49:1403996:50:mbed:10:506817:7:9:14:4690:19:1:51:45970557,58046687,54804607,47611766,54444684,44062068,32885972,37259527,59626284
,54790575,50258689,80252396:55:50:56:4:28:1703035896:29:0|1:38147:2:Dream Sequencer:3:RGlkIEkgZHJlYW0gb2YgdGhpcyBiZWZvcmU_:5:1:49:883621:50:Jghost:10:343294:7:5:14:4618:19:1:51:286
7632,55644122,46352736,57784142,51939013,54724490,95241558,62868423,61631083,76016356:55:35:56:7:28:1703251245:29:0|1:24719:2:The Nine Circles:3:TmluZSBvZiB0aGUgbW9zdCBjbGFzc2ljIE5
pbmUgQ2lyY2xlcyBsZXZlbHMgZnJvbSB1cGRhdGUgMS45ISBPcmdhbml6ZWQgcm91Z2hseSBieSBkaWZmaWN1bHR5Lg==:5:3:49:57903:50:Ryder:10:203747:7:8:14:3793:19:1:51:7116121,6892453,4284013,6939821,69
88264,7018102,5310094,8723596,7054561:55:80:56:5:28:1703144410:29:1703394420|1:20917:2:Nostalgia:3:T25lIG9mIHRoZSBiZXN0IGxldmVscyBvZiB0aGUgMS45LzIuMCBlcmEu:5:1:49:1711800:50:MrSpag
hetti:10:140165:7:4:14:3788:19:1:51:11214476,8477262,5298301,11357573,2952064,3186219,27106043,12676943,21395297,4604249,10234384,3435257,4141864,3382569,4839503,2915652,2850773,44
96520,3065291,10541049,13529177,12057578,3757912,3010126,11849346:55:50:56:15:28:1703117941:29:0#1078150:ViPriN:2795|3713125:Ryder:57903|7072936:Jghost:883621|7254885:AutoNick:1093
804|8599996:Subwoofer:1275405|7381956:mbed:1403996|2989276:MrSpaghetti:1711800|15479163:tricipital:6061424|125375460:BLEACHwav:12308929#9999:0:10#f5da5823d94bbe7208dd83a30ff427c7d88fdb99
"""