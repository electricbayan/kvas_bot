from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from config import settings
from api.database.models import Base, User, Admin, Creator
import asyncio
from src.exceptions import UserNotFound


engine = create_async_engine(
    url=settings.DATABASE_URL,
)
session_factory = async_sessionmaker(engine)


class Database:
    @staticmethod
    async def create_tables() -> None:
        async with engine.begin() as con:
            await con.run_sync(Base.metadata.drop_all)
            await con.run_sync(Base.metadata.create_all)
            
    @staticmethod
    async def insert_user(tg_id: str, lang="ru") -> None:
        
        async with session_factory() as session:
            user = await session.get(User, {'tg_id': tg_id})
            if not user:
                dataobj = User(tg_id=tg_id, lang=lang)
                session.add(dataobj)
            else:
                user.lang=lang
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def get_language(tg_id: str) -> None:
        try:
            async with session_factory() as session:
                user = await session.get(User, {'tg_id': str(tg_id)})
                return user.lang
        except AttributeError:
            return "en"
    
    @staticmethod
    async def get_free_creator(work_type):
        pass

    @staticmethod
    async def add_creator(tg_id: str, skill: str) -> None:
        async with session_factory() as session:
            creator = await session.get(Creator, {'tg_id': tg_id})
            if not creator:
                dataobj = Creator(tg_id=tg_id, skill=skill)
                session.add(dataobj)
            await session.flush()
            await session.commit()

    @staticmethod
    async def remove_creator():
        pass

    @staticmethod
    async def add_admin(tg_id: str) -> None:
        async with session_factory() as session:
            admin = await session.get(Admin, {'tg_id': tg_id})
            if not admin:
                dataobj = Admin(tg_id=tg_id)
                session.add(dataobj)
            await session.flush()
            await session.commit()

    @staticmethod
    async def remove_admin(tg_id: str) -> None:
        async with session_factory() as session:
            admin = await session.get(Admin, {'tg_id': tg_id})
            if admin:
                await session.delete(admin)
                await session.flush()
                await session.commit()
            else:
                raise UserNotFound
    

async def main():
    async with engine.connect() as con:
        res = await con.execute(text("SELECT * FROM users"))
        print(res.fetchone())


if __name__ == "__main__":
    asyncio.run(main())