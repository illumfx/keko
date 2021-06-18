from tortoise import Tortoise
import asyncio
import platform

async def init_db(env) -> None:
    """Connect to the postgres database using environ
    """
    for _ in range(5):
        try:
            await Tortoise.init(
                #db_url=f"postgres://{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}@{env.POSTGRES_HOST}/{env.POSTGRES_DB}",
                db_url=env.DB_URL,
                modules={"models": ["bot.models"]}
            )  
        except:
            await asyncio.sleep(1.5)
    else:
        await Tortoise.generate_schemas()