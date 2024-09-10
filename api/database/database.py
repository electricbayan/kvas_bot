from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy import text, select, and_
from config import settings
from api.database.models import Base, User, Admin, Creator, SkillType, CreatorSkillType, Order, UniqueToken
from src.exceptions import UserNotFound
from random import randint


engine = create_async_engine(
    url=settings.DATABASE_URL,
)
session_factory = async_sessionmaker(engine)

prices = {
    'mod_skill': 10,
    'vanil_skin_skill': 140,
    'pastel_skin_skill': 140,
    'building_location_skill': 300,
    'single_building_skill': 150,
    '2d_totem_skill': 20,
    '3d_totem_skill': 50,
    'custom_totem_skill': 90,
    'art_with_background_skill': 590,
    'art_without_background_skill': 270,
    'mob_skill': 150,
    'item_skill': 60,
    'logo_skill': 300,
    'registration_skill': 150
}


class Database:
    @staticmethod
    async def create_tables() -> None:
        async with engine.begin() as con:
            await con.run_sync(Base.metadata.drop_all)
            await con.run_sync(Base.metadata.create_all)
        async with session_factory() as session:
            for ordertype in prices.keys():
                dataobj = SkillType(name=ordertype, price=prices[ordertype])
                session.add(dataobj)
            dataobj = UniqueToken(last_value = '3810920946')
            session.add(dataobj)
            await session.flush()
            await session.commit()

            
    @staticmethod
    async def insert_user(tg_id: str, lang="ru", url=None) -> None:
        async with session_factory() as session:
            user = await session.get(User, {'tg_id': tg_id})
            if not user:
                dataobj = User(tg_id=tg_id, lang=lang, url=url)
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
    async def add_creator(tg_id: str, username: str, skill: str) -> None:
        async with session_factory() as session:
            creator = await session.get(Creator, {'tg_id': tg_id})
            statement = select(SkillType).filter_by(name=skill)
            print(f'{skill=}')
            skill_obj = await session.scalars(statement)
            skill_id = skill_obj.one().id
            if not creator:
                creator_dataobj = Creator(tg_id=tg_id, is_busy=True, username=username)
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
            order = await session.get(Order, {'id': order_id})
            order.creator_id = creator_id
            order.is_payed = True
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
        
    async def change_creator_business(self, tg_id: str, business: bool) -> dict:
        async with session_factory() as session:
            creator = await session.get(Creator, {'tg_id': tg_id})
            creator.is_busy = business
            order_id = None
            if not business:
                
                subq = select(CreatorSkillType.skilltype_id).where(CreatorSkillType.creator_id==creator.tg_id)
                skilltype_ids = await session.execute(subq)
                skilltype_ids = skilltype_ids.all()
                skilltype_ids = [i[0] for i in skilltype_ids]
                orders_subq = select(SkillType.name).where(SkillType.id.in_(skilltype_ids))
                skilltypes = await session.execute(orders_subq)
                skilltypes = skilltypes.all()
                skilltypes = [i[0] for i in skilltypes]

                query = select(Order).where(and_(Order.is_payed==True, Order.order_type.in_(skilltypes)))
                orders = await session.execute(query)
                obj_db = orders.scalars()
                if obj_db:
                    order = obj_db.first()
                    order_id = order.id # 
                    await self.add_creator_to_order(str(tg_id), order.id)
            await session.flush()
            await session.commit()
            return order_id

    @staticmethod
    async def get_creator_offers(tg_id: str):
        async with session_factory() as session:
            stmt = select(Order).where(Order.creator_id == tg_id)
            orders = await session.execute(stmt)
            order_list = []
            orders = orders.scalars().all()
            for order in orders:
                order_list.append(order)
            return order_list
        
    @staticmethod
    async def get_user_orders(tg_id: str):
        async with session_factory() as session:
            stmt = select(Order).where(Order.customer_id == tg_id)
            orders = await session.execute(stmt)
            order_list = []
            orders = orders.scalars().all()
            for order in orders:
                order_list.append(order)
            return order_list
        
    @staticmethod
    async def get_order(order_id: int) -> Order:
        async with session_factory() as session:
            order = await session.get(Order, {'id': order_id})
        return order


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
            price = price.scalar()

            stmt = select(Order).where(Order.token == token)
            order = await session.execute(stmt)
            order = order.scalars().one()

            subq = (select(Creator.tg_id).where(Creator.is_busy==False))
            creators = await session.execute(subq)
            creators = creators.first()
            subq = select(Order.order_type).where(Order.token == token)
            ordertype = await session.execute(subq)
            ordertype = ordertype.first()

            subq = select(SkillType.id).where(SkillType.name.in_(ordertype))
            skilltype_id = await session.execute(subq)
            skilltype_id = skilltype_id.first()
            print('FUNCTIONING')
            try:
                if not creators:
                    raise NoResultFound
                stmt = select(CreatorSkillType.creator_id).where(and_(CreatorSkillType.skilltype_id.in_(skilltype_id), CreatorSkillType.creator_id.in_(creators)))
                result = await session.execute(stmt)
                creator_id = result.scalar()
                stmt = select(Creator.username).where(Creator.tg_id==creator_id)
                creator_username = await session.execute(stmt)
                creator_username = creator_username.scalar()
                await self.add_creator_to_order(creator_id=creator_id, order_id=order.id)
                return order, creator_id, price, creator_username
            except NoResultFound:
                print('EXCEPTION')
                await self.set_payed_status(True, order.id)
                return order, None, price, None
        
    @staticmethod
    async def set_payed_status(status, order_id):
        async with session_factory() as session:
            order = await session.get(Order, {'id': order_id})
            order.is_payed = True
            await session.flush()
            await session.commit()

    @staticmethod
    async def get_profit() -> dict:
        async with session_factory() as session:
            stmt = select(Creator.tg_id)
            creators_id = await session.execute(stmt)
            creators_id = creators_id.scalars().all()

            creators_profit = {}
            print(creators_id)
            for creator_id in creators_id:
                stmt = select(Order.order_type).where(Order.creator_id==creator_id)
                ordertype = await session.execute(stmt)
                price = prices[ordertype.scalar()]

                stmt = select(Creator.username).where(Creator.tg_id==creator_id)
                userid = await session.execute(stmt)
                userid = userid.scalar()

                if userid in creators_profit.keys():
                    creators_profit[userid] += price
                else:
                    creators_profit[userid] = price
            return creators_profit
