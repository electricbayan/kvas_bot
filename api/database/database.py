from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import URL, text
from config import settings
from api.database.models import Base, User
import asyncio


engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)
session_factory = async_sessionmaker(engine)


class Database:
    @staticmethod
    async def create_tables():
        async with engine.begin() as con:
            await con.run_sync(Base.metadata.drop_all)
            await con.run_sync(Base.metadata.create_all)

    async def insert_user(self, tg_id, lang="ru"):
        async with session_factory() as session:
            dataobj = User(tg_id=tg_id, lang=lang)
            session.add(dataobj)
            await session.commit()
    
    async def edit_language():
        pass
    

async def main():
    async with engine.connect() as con:
        res = await con.execute(text("SELECT * FROM users"))
        print(res.fetchone())


if __name__ == "__main__":
    asyncio.run(main())