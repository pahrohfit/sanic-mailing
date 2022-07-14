from pathlib import Path

import fakeredis.aioredis
import pytest
from sanic import Sanic, response
from sanic.exceptions import SanicException

from sanic_mailing.utils import DefaultChecker


@pytest.fixture
def default_checker():
    test = DefaultChecker()
    yield test
    del test


@pytest.fixture
async def redis_checker(scope="redis_config"):
    test = DefaultChecker(db_provider="redis")
    test.redis_client = fakeredis.aioredis.FakeRedis()
    yield test
    await test.redis_client.flushall()
    await test.close_connections()


@pytest.fixture
def mail_config():
    home: Path = Path(__file__).parent.parent
    html = home / "files"
    env = {
        "MAIL_USERNAME": "example@test.com",
        "MAIL_PASSWORD": "strong",
        "MAIL_FROM": "example@test.com",
        "MAIL_FROM_NAME": "example",
        "MAIL_PORT": 25,
        "MAIL_SERVER": "localhost",
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": False,
        "MAIL_DEBUG": 0,
        "SUPPRESS_SEND": 1,
        "USE_CREDENTIALS": False,
        "VALIDATE_CERTS": False,
        "MAIL_TEMPLATE_FOLDER": html,
    }

    return env


@pytest.fixture
def app(mail_config) -> Sanic:
    sanic_app = None
    try:
       sanic_app = Sanic(__name__)
    except SanicException:
        sanic_app = Sanic.get_app()
        return sanic_app
    sanic_app.config.SECRET_KEY = "top-secret-key"
    sanic_app.config['PYTESTING'] = True
    sanic_app.config.TESTING = True
    sanic_app.config.update(mail_config)

    @sanic_app.get("/")
    def basic(request):
        return response.text("foo")

    return sanic_app
