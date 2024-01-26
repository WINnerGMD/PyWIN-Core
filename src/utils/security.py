from .. depends.context import Context

"""JWT and GJP authentication"""


async def checkValidGJP2(ctx: Context, id: int, gjp2: str) -> bool:
    """
    Check Geometry Dash Password 2
    """

    try:
        user = await ctx.database.users.find_byid(id)
        if user.passhash == gjp2:
            return True
        else:
            return False
    except:
        return False
