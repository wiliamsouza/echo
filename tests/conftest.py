# coding: utf-8

import pytest

import aioredis

from echo import api


@pytest.yield_fixture()
def redis_flush(event_loop):
    redis = yield from aioredis.create_redis(('127.0.0.1', 6379))

    yield redis
    yield from redis.flushdb()
    redis.close()


@pytest.yield_fixture()
def api_server(event_loop, unused_tcp_port):
    tcp_port = unused_tcp_port
    server, handler, redis_pool = event_loop.run_until_complete(
        api.start(event_loop, tcp_port))

    yield 'http://127.0.0.1:{}/'.format(tcp_port)
    event_loop.run_until_complete(handler.finish_connections(1.0))
    event_loop.run_until_complete(redis_pool.clear())
    api.stop(event_loop)