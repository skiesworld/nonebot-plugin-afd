import json
from pathlib import Path

from nonebot.adapters.afdian import OrderNotifyEvent
from nonebot.compat import type_validate_python
from nonebug import App
import pytest


@pytest.mark.asyncio
async def test_webhook_test_order(app: App):
    from nonebot_plugin_afd.order_notice import order_handler

    file_path = Path(__file__).parent / "events.json"

    with open(file_path, encoding="utf-8") as f:  # noqa: ASYNC230
        test_data = json.load(f)

    event = type_validate_python(OrderNotifyEvent, test_data)

    async with app.test_matcher(order_handler) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_ignore_rule(order_handler)
