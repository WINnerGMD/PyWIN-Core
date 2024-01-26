from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. models import FeaturedLevelsModel


class DailyService:
    @staticmethod
    async def getCountDailyLevels(db: AsyncSession) -> int:
        """Total count of Daily levels"""

        models = (
            (
                await db.execute(
                    select(FeaturedLevelsModel).filter(FeaturedLevelsModel.type == 1)
                )
            )
            .scalars()
            .all()
        )

        return len(models)

    @staticmethod
    async def getCountWeeklyLevels(db: AsyncSession) -> int:
        """Total count of Weekly levels"""

        models = (
            (
                await db.execute(
                    select(FeaturedLevelsModel).filter(FeaturedLevelsModel.type == 2)
                )
            )
            .scalars()
            .all()
        )

        return len(models)

    @staticmethod
    async def getLastDaily(db: AsyncSession) -> FeaturedLevelsModel:
        """Get last Daily level for users"""

        model = (
            (
                await db.execute(
                    select(FeaturedLevelsModel)
                    .filter(FeaturedLevelsModel.type == 1)
                    .order_by(FeaturedLevelsModel.id.desc())
                )
            )
            .scalars()
            .first()
        )

        return model

    @staticmethod
    async def getLastWeekly(db: AsyncSession) -> FeaturedLevelsModel:
        """Get last Daily level for users"""

        model = (
            (
                await db.execute(
                    select(FeaturedLevelsModel)
                    .filter(FeaturedLevelsModel.type == 2)
                    .order_by(FeaturedLevelsModel.id.desc())
                )
            )
            .scalars()
            .first()
        )

        return model
