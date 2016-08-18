import asyncio

import sys

from models import User, ZhitiaoItem
from orm import select, create_pool, execute


async def test(loop):
    await create_pool(loop=loop, host='127.0.0.1', user='root', password='1234', db='zhitiao')
    u = await User.find(email='88888888@qq.com')
    k = ZhitiaoItem(keywords='i,am,the,king', distance=100, num=3, lng='12.9999', lat='76.3333', alt='1.555', owner=u.id)
    await k.save()
    print(k)


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
if loop.is_closed():
    sys.exit(0)
