from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from logger import error
from src.services.comments import PostCommentsService
from src.models import UsersModel
from src.utils.gdform import gd_dict_str


class UserObject:
    def __init__(self, service: UsersModel):
        self.service = service

    async def request_access(self):
        return self.service["permissions"].typeMod

    async def GDGetUser(self):
        try:
            user = self.service
            iconkit = user.iconkits
            response_strs = gd_dict_str(
                {
                    1: user.userName,
                    2: user.id,
                    3: user.stars,
                    4: user.demons,
                    5: 20,
                    6: 1,
                    8: user.cp,
                    10: iconkit["color1"],
                    11: iconkit["color2"],
                    13: user.coins,
                    14: 1,
                    15: 1,
                    16: user.id,
                    17: user.usr_coins,
                    21: iconkit["accIcon"],
                    22: iconkit["accShip"],
                    23: iconkit["accBall"],
                    24: iconkit["accBird"],
                    25: iconkit["accDart"],
                    26: iconkit["accRobot"],
                    28: iconkit["accGlow"],
                    29: 1,
                    30: 1,
                    43: iconkit["accSpider"],
                    44: "",
                    45: "",
                    46: user.diamonds,
                    48: 1,
                    49: 4,
                    52: 890
                }
            )
            return response_strs
        except Exception as ex:
            error(ex)

    async def GDGetUserPosts(self, page):
        post_string = []
        service = await PostCommentsService().get_post(
            usrid=self.service.id, page=page
        )
        for post in service["database"]:
            try:
                time = datetime.strptime(post.timestamp, "%Y-%m-%d %H:%M:%S.%f")
            except:
                time = datetime(1, 1, 1, 1, 1, 1, 1)
            post_string.append(
                gd_dict_str(
                    {
                        # f"1~{i.lvllink}~2~{i.content}~3~{i.accountID}~4~{i.likes}~10~{i.percent}~9~{time.day}/{time.month}/{time.year} {time.second}:{time.minute}~6~{i.id}|"\
                        1: post.lvllink,
                        2: post.content,
                        3: post.accountID,
                        4: post.likes,
                        6: post.id,
                        9: f"{time.day}/{time.month}/{time.year} {time.second}:{time.minute}",
                        10: post.percent,
                    },
                    separator="~",
                )
            )
        offset = page * 10
        return "|".join(post_string) + f"#{service['count']}:{offset}:10"
        # iconkit = user_obj.iconkits
        # rank  = len((await db.execute(select(models.Users).filter(models.Users.stars >= user_obj.stars))).scalars().all())
        # modlevel = (await PermissionService().get_permissions(id=user_obj.role,db=db)).BadgeID
        # response = f'1:{user_obj.userName}:2:{user_obj.id}:13:{user_obj.coins}:17:{user_obj.usr_coins}:10:{iconkit["color1"]}:11:{iconkit["color2"]}:3:{user_obj.stars}:46:{user_obj.diamonds}:4:{user_obj.demons}:8:{user_obj.cp}:18:0:19:0:50:0:20::21:{iconkit["accIcon"]}:22:{iconkit["accShip"]}:23:{iconkit["accBall"]}:24:{iconkit["accBird"]}:25:{iconkit["accDart"]}:26:{iconkit["accRobot"]}:28:{iconkit["accGlow"]}:43:{iconkit["accSpider"]}:48:1:30:{rank}:16:{user_obj.id}:31:0:44::45::49:{modlevel}:29:1'
        # return response


class UserGroup:
    def __init__(self, service):
        self.service = service

    async def GDGetUserGroup(self):
        users_string = []
        count = 1
        for user in self.service["database"]:
            iconkit = user.iconkits
            users_string.append(
                gd_dict_str(
                    {
                        1: user.userName,
                        2: user.id,
                        3: user.stars,
                        4: user.demons,
                        6: count,
                        7: user.id,
                        8: user.cp,
                        9: iconkit["accIcon"],
                        10: iconkit["color1"],
                        11: iconkit["color2"],
                        13: user.coins,
                        14: 0,
                        16: user.id,
                        17: user.usr_coins,
                    }
                )
            )
            count += 1
        return "|".join(users_string) + "#999:0:10"

    # string += f"1:{i.userName}:2:{i.id}:3:{i.stars}:4:{i.demons}:6:{count}:7:{i.id}:8:{i.cp}:9:{iconkit['accIcon']}:10:{iconkit['color1']}:11:{iconkit['color2']}:13:{i.coins}:14:0:15:{i.id}:16:{i.id}:17:{i.usr_coins}:46:{i.diamonds}|"
