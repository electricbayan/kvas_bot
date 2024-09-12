from api.database.database import Database
import asyncio

db = Database()
async def main():
    await db.reset_db()


if __name__ == "__main__":
    asyncio.run(main())