import asyncio
from . import client

bot = client.RoboDuck()

# async def run():  
#     try:
#         await bot.start()
#     except:
#         await bot.close()
        
#asyncio.run(run())

bot.run()