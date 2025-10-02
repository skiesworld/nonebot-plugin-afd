import nonebot
from nonebot.adapters.afdian import Adapter as AFDianAdapter
from nonebot.adapters.onebot.v11 import Adapter as OnebotAdapter
from nonebug import NONEBOT_INIT_KWARGS
import pytest
from pytest_asyncio import is_async_test


def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi+~httpx",
        "log_level": "DEBUG",
        "afd_token_dict": {222222222: ["85ee9c02255d11eb9d0852540025c377"]},
    }


def pytest_collection_modifyitems(items: list[pytest.Item]):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session", autouse=True)
async def after_nonebot_init(after_nonebot_init: None):
    driver = nonebot.get_driver()
    driver.register_adapter(AFDianAdapter)
    driver.register_adapter(OnebotAdapter)
    nonebot.load_from_toml("pyproject.toml")
