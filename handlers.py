import functools
import hashlib
import json
import re

from aiohttp import web
from flask import jsonify

from coroweb import get, post, put, Auth
from keyvalue import redis
from models import User, ZhitiaoItem


def url_for(request, endpoint, **values):
    item = globals().get(endpoint)
    __regex = re.compile(r'\{\w+\}')
    if item is not None and hasattr(item, '__call__'):
        path = item.__route__
        path = path.split('/')
        i = 0
        for x in path:
            if __regex.match(x):
                for k, v in values.items():
                    if x[1:-1] == k:
                        path[i] = v
            i += 1
        return request.scheme + '://' + request.host + '/'.join(path)
    return None


@post('/login')
async def login(request, *, username, password):
    if username == 'aaa' and password == '123':
        sha1 = hashlib.sha1()
        sha1.update(username.encode('utf-8'))
        sha1.update(b':')
        sha1.update(password.encode('utf-8'))
        token = sha1.hexdigest()
        redis.set('user:aaa', token)
        redis.set(token, 'user:aaa')
        return token


@get('/api/users/{name}/s/{num}')
async def get_user(name, num):
    user = await User.find(name=name)
    if user:
        return {
            'name' + num: user.name[:int(num)]
        }


@get('/zhitiaos')
async def get_zhitiaos(request):
    zhitiaos = await ZhitiaoItem.findAll()
    for zhitiao in zhitiaos:
        zhitiao.url = url_for(request, 'get_zhitiao', id=zhitiao.id)

    return zhitiaos


@get('/zhitiaos/{id}')
async def get_zhitiao(id):
    zhitiao = await ZhitiaoItem.findByPk(id)
    return zhitiao


@post('/zhitiaos')
async def create_zhitiao(request, *, keywords, distance, num, owner, lng=None, lat=None, alt=None):
    if not request.json:
        print('不是josn')
    zhitiao = ZhitiaoItem(keywords=keywords, distance=distance, num=num, owner=owner, lng=lng, lat=lat, alt=alt)
    rows = await zhitiao.save()
    return str(rows)


@put('/zhitiaos/{id}')
async def update_zhitiao(id, request, *, keywords, distance, num, owner, lng=None, lat=None, alt=None):
    if not request.json:
        print('不是json')
    zhitiao = await ZhitiaoItem.findByPk(id)
    zhitiao.keywords = keywords
    zhitiao.distance = distance
    zhitiao.num = num
    zhitiao.owner = owner
    zhitiao.lng = lng
    zhitiao.lat = lat
    zhitiao.alt = alt
    rows = await zhitiao.update()
    status = 202 if rows == 1 else 400
    return {
        'status': status,
        'rows': rows
    }


@Auth(False)
@get('/zhitiaos/user/{id}')
async def getSomeoneZhitiao(id):
    zhitiaos = await ZhitiaoItem.findAll('owner=?', [id])
    return zhitiaos

    # @delete('/zhitiaos/{id}')
    # async def delete(zhitiao):
    #
