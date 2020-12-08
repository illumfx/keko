from tortoise import Tortoise
import asyncio
import platform

async def init_db(env) -> None:
    """Connect to the postgres database using environ
    """
    for _ in range(5):
        try:
            await Tortoise.init(
                db_url=f"postgres://keko:{env.POSTGRES_PASSWORD}@database/keko" if platform.system() == "Linux" else f"postgres://keko:{env.POSTGRES_PASSWORD}@localhost/keko",
                modules={"models": ["bot.models"]}
            )  
        except:
            await asyncio.sleep(1.5)
    else:
        await Tortoise.generate_schemas()