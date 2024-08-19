from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text, select
from config import settings
from api.database.models import Base, User, Admin, Creator, SkillType, CreatorSkillType, Order
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
        async with session_factory() as session:
            for ordertype in ('mods_skill', 'drawing_skill', '3d_skill', 'resources_skill'):
                dataobj = SkillType(name=ordertype)
                session.add(dataobj)
            await session.flush()
            await session.commit()

            
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
            statement = select(SkillType).filter_by(name=skill)
            skill_obj = await session.scalars(statement)
            skill_id = skill_obj.one().id
            if not creator:
                creator_dataobj = Creator(tg_id=tg_id)
                skillrelation_obj = CreatorSkillType(skilltype_id=skill_id, creator_id=creator_dataobj.tg_id)
                session.add(creator_dataobj)
                session.add(skillrelation_obj)
            await session.flush()
            await session.commit()

    @staticmethod
    async def remove_creator(tg_id: str):
        async with session_factory() as session:
            creator = await session.get(Creator, {'tg_id': tg_id})
            # statement = select(CreatorSkillType).filter_by(creator_id=tg_id)
            # creator_skills = await session.scalars(statement)
            if not creator:
                raise UserNotFound
            else:
                # for creator_skills_obj in creator_skills.all():
                #     await session.delete(creator_skills_obj)
                await session.delete(creator)
                await session.flush()
                await session.commit()

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
            

    @staticmethod
    async def add_payment(customer_id: str, offer_type: str, description: str, amount: str):
        async with session_factory() as session:
            dataobj = Order(customer_id=customer_id, order_type=offer_type, description=description, amount=amount)
            session.add(dataobj)
            await session.flush()
            await session.commit()
    

async def main():
    async with engine.connect() as con:
        res = await con.execute(text("SELECT * FROM users"))
        print(res.fetchone())


if __name__ == "__main__":
    asyncio.run(main())