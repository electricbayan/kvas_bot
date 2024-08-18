from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from config import settings
from api.database.models import Base, User, Admin
import asyncio


engine = create_async_engine(
    url=settings.DATABASE_URL,
)
session_factory = async_sessionmaker(engine)

class UserNotFound(Exception):
    pass


class Database:
    @staticmethod
    async def create_tables():
        async with engine.begin() as con:
            await con.run_sync(Base.metadata.drop_all)
            await con.run_sync(Base.metadata.create_all)

    async def insert_user(self, tg_id: str, lang="ru"):
        
        async with session_factory() as session:
            user = await session.get(User, {'tg_id': tg_id})
            if not user:
                dataobj = User(tg_id=tg_id, lang=lang)
                session.add(dataobj)
            else:
                user.lang=lang
            await session.flush()
            await session.commit()
    
    async def get_language(self, tg_id: str):
        try:
            async with session_factory() as session:
                user = await session.get(User, {'tg_id': str(tg_id)})
                return user.lang
        except AttributeError:
            return "en"
        
    async def get_free_creator(self, work_type):
        pass


    async def add_creator(self):
        pass

    async def add_admin(self, tg_id: str):
        async with session_factory() as session:
            admin = await session.get(Admin, {'tg_id': tg_id})
            if not admin:
                dataobj = Admin(tg_id=tg_id)
                session.add(dataobj)
            await session.flush()
            await session.commit()

    async def remove_admin(self, tg_id: str):
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