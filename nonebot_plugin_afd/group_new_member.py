import hashlib
import json
import time
from typing import Union

import httpx
from nonebot import on_request
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupRequestEvent

from . import config

new_member = on_request()


@new_member.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    comment = event.comment
    if event.sub_type == "add" and comment:
        if "\n答案：" in comment:
            comment = comment[comment.find("\n答案：") + 4:]

        if order_event := await call_order_api(event.group_id, comment):
            try:
                if order_event["data"]["list"]:
                    await event.approve(bot)
            except KeyError:
                pass


async def call_order_api(group_id: Union[str, int], order_id: str):
    """爱发电 订单查询 API"""
    if not config.afd_token_list:
        return None
    try:
        user_id = config.afd_token_list[str(group_id)]["user_id"]
        token = config.afd_token_list[str(group_id)]["token"]
    except KeyError:
        return None
    params_json = json.dumps({"out_trade_no": order_id})
    ts = int(time.time())
    """当前时间戳"""

    sign_str = f"{token}params{params_json}ts{ts}user_id{user_id}"
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()

    async with httpx.AsyncClient() as client:
        data = await client.get(
            url="https://afdian.net/api/open/query-order",
            params={
                "user_id": user_id,
                "params": params_json,
                "ts": ts,
                "sign": sign
            }
        )
    return data.json()
