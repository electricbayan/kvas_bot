from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy import text, select, and_
from config import settings
from api.database.models import Base, User, Admin, Creator, SkillType, CreatorSkillType, Order, UniqueToken
import asyncio
from src.exceptions import UserNotFound
from random import randint


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
            skilltypes = ('vanil_skin', 'pastel_skin', 'building_location', 'single_building', '2d_totem', '3d_totem', 'custom_totem', 'art_with_background', 'art_without_background', 'mob', 'item', 'mod')
            prices = [10] * 11
            for ordertype, price in zip(skilltypes, prices):
                dataobj = SkillType(name=ordertype + "_skill", price=price)
                session.add(dataobj)
            dataobj = UniqueToken(last_value = '3810920946')
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
    async def get_token() -> None:
        async with session_factory() as session:
            statement = text("""SELECT last_value FROM token""")
            res = await session.execute(statement)
        return res.one()
    
    @staticmethod
    async def update_token(new_value: str) -> None:
        async with session_factory() as session:
            tkn = await session.get(UniqueToken, {'id': 1})
            tkn.last_value = new_value
            await session.flush()
            await session.commit()

    @staticmethod
    async def add_creator(tg_id: str, skill: str) -> None:
        async with session_factory() as session:
            creator = await session.get(Creator, {'tg_id': tg_id})
            statement = select(SkillType).filter_by(name=skill)
            skill_obj = await session.scalars(statement)
            skill_id = skill_obj.one().id
            if not creator:
                creator_dataobj = Creator(tg_id=tg_id, is_busy=True)
                skillrelation_obj = CreatorSkillType(skilltype_id=skill_id, creator_id=creator_dataobj.tg_id)
                session.add(creator_dataobj)
                session.add(skillrelation_obj)
            else:
                skillrelation_obj = CreatorSkillType(skilltype_id=skill_id, creator_id=creator.tg_id)
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
    async def add_creator_to_order(creator_id: str, order_id: int):
        async with session_factory() as session:
            order = await session.get(Order, {'id': id})
            order.creator_id = creator_id
            await session.flush()
            await session.commit()

    @staticmethod
    async def is_user_creator(tg_id: str) -> bool:
        async with session_factory() as session:
            creator = await session.get(Creator, {'tg_id': tg_id})
            return bool(creator)
        
    @staticmethod
    async def is_creator_busy(tg_id: str) -> bool:
        async with session_factory() as session:
            creator = await session.get(Creator, {'tg_id': tg_id})
            return bool(creator.is_busy)
        
    @staticmethod
    async def change_creator_business(tg_id: str, business: bool):
        async with session_factory() as session:
            creator = await session.get(Creator, {'tg_id': tg_id})
            creator.is_busy = business
            if not business:
                # ДОПИСАТЬ stmt
                stmt = select(Order).where(and_(Order.creator_id is None, Order.order_type.in_(select(SkillType.name).where())))
            await session.flush()
            await session.commit()

    @staticmethod
    async def get_creator_offers(tg_id: str):
        async with session_factory() as session:
            print(tg_id)
            stmt = select(Order).where(Order.creator_id == tg_id)
            orders = await session.execute(stmt)
            order_list = []
            orders = orders.scalars().all()
            print(orders)
            for order in orders:
                order_list.append(order)
            return order_list


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
    async def add_payment(customer_id: str, offer_type: str, description: str, token:str):
        async with session_factory() as session:
            dataobj = Order(customer_id=customer_id, order_type=offer_type, description=description, token=token)
            session.add(dataobj)
            await session.flush()
            await session.commit()

    async def confirm_payment(self, token):
        async with session_factory() as session:
            stmt = select(SkillType.price).where(SkillType.name.in_(select(Order.order_type).where(Order.token == token)))
            price = await session.execute(stmt)
            price = price.scalars().one()
            stmt = select(Order).where(Order.token == token)
            order = await session.execute(stmt)
            order = next(order.scalars())

            stmt = select(CreatorSkillType.creator_id).where(and_(CreatorSkillType.skilltype_id.in_(select(SkillType.id).where(SkillType.name.in_(select(Order.order_type).where(Order.token == token)))), CreatorSkillType.creator_id.in_(select(Creator.tg_id).where(Creator.is_busy==False))))
            result = await session.execute(stmt)
            try:
                creator_id = result.one()
                self.add_creator_to_order(creator_id=creator_id, order_id=order.id)
                return order, creator_id, price
            except NoResultFound:
                return order, None, price
    
    

async def main():
    async with engine.connect() as con:
        res = await con.execute(text("SELECT * FROM users"))
        print(res.fetchone())


if __name__ == "__main__":
    asyncio.run(main())