import time

import nonebot
from nonebot.adapters.afdian import Adapter as AFDianAdapter
from nonebot.adapters.afdian import Bot as AFDianBot
from nonebot.adapters.onebot.v11 import Adapter as OneBotAdapter
from nonebot.adapters.onebot.v11 import Bot as OneBot
from nonebot.adapters.onebot.v11 import GroupRequestEvent
from nonebug import App
import pytest


@pytest.mark.asyncio
async def test_new_member(app: App):
    # 导入你的事件处理器
    from nonebot_plugin_afd.group_new_member import new_member

    # 创建事件
    event = GroupRequestEvent(
        time=int(time.time()),
        self_id=111111111,
        post_type="request",
        request_type="group",
        sub_type="add",
        group_id=222222222,
        user_id=333333333,
        comment="202507151838275197991024299",
        flag="test_flag_123",
    )

    # 使用测试上下文
    async with app.test_matcher(new_member) as ctx:
        afdian_adapter = nonebot.get_adapter(AFDianAdapter)
        ctx.create_bot(
            base=AFDianBot,
            adapter=afdian_adapter,
            self_id="85ee9c02255d11eb9d0852540025c377",
        )

        onebot_adapter = nonebot.get_adapter(OneBotAdapter)
        one_bot = ctx.create_bot(
            base=OneBot, adapter=onebot_adapter, self_id="111111111"
        )
        ctx.receive_event(one_bot, event)
        ctx.should_call_api(
            api="query_order_by_out_trade_no",
            data={
                "out_trade_no": "202507151838275197991024299",
            },
            result=None,
            adapter=afdian_adapter,
        )

        ctx.should_call_api(
            api="set_group_add_request",
            data={
                "flag": event.flag,
                "sub_type": event.sub_type,
                "approve": True,
                "reason": "同意进群",
            },
            result=None,
            adapter=onebot_adapter,
        )
        ctx.should_finished(new_member)
