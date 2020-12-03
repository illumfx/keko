from tortoise import Tortoise
from asyncio import sleep

async def init_db(env):
    """Connect to the postgres database using environ
    """
    for _ in range(5):
        try:
            await Tortoise.init(
                db_url=f"postgres://keko:{env.POSTGRES_PASSWORD}@database/keko",
                modules={"models": ["bot.models"]}
            )  
        except:
            await sleep(1)
    else:
        await Tortoise.generate_schemas()