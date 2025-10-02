import asyncio

from nonebot import get_bots, logger, on_notice
from nonebot.adapters.afdian import Bot, OrderNotifyEvent
from nonebot.adapters.onebot.v11 import Bot as OneBot

from .utils import afdian_bot_id_to_group_ids, get_description, user_ids


def afdian_rule(bot: Bot) -> bool:
    return bot.self_id in user_ids


order_handler = on_notice(rule=afdian_rule)


@order_handler.handle()
async def handle_afdian_order(bot: Bot, event: OrderNotifyEvent):
    logger.info(
        f"[爱发电 | 通知] 作者：{bot.self_id[:5]}{'*' * 5} 有新的订单 {event.get_order().out_trade_no} 来自用户 {event.get_user_id()}"
    )

    notice_text = get_description(bot.self_id, event)

    logger.info(notice_text)

    logger.info("正在寻找可用Bot")

    group_list = afdian_bot_id_to_group_ids[bot.self_id]

    qqbot: OneBot | None = None
    for temp_bot in get_bots().values():
        if isinstance(temp_bot, OneBot):
            qqbot = temp_bot
            break
    else:
        logger.warning("未找到可用的OneBot适配器Bot，无法发送订单通知")
        return

    tasks: list[asyncio.Task] = []
    for group_id in group_list:
        task = asyncio.create_task(
            qqbot.send_group_msg(group_id=group_id, message=notice_text)
        )
        tasks.append(task)
    await asyncio.gather(*tasks)
    logger.info("所有订单通知发送完成")
