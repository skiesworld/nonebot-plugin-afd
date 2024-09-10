from nonebot import logger, on_notice
from nonebot.adapters.afdian import Bot, OrderNotifyEvent
from nonebot.exception import FinishedException

from . import config


def afdian_rule(event: OrderNotifyEvent) -> bool:
    return event.get_user_id() in set(config.afd_token_dict.values())


order_handler = on_notice(rule=afdian_rule)


@order_handler.handle()
async def handle_afdian_order(bot: Bot, event: OrderNotifyEvent):
    notice_text = (
        f"作者：{bot.bot_info.user_id[:5]}{'*' * 5} 有新的订单\n"
        f"{'=' * 15}\n"
        f"用户ID：{event.get_user_id()[:5]}{'*' * 5}\n"
        f"订单号：{event.data.order.out_trade_no[:5]}{'*' * 5}\n"
        f"发电 {event.data.order.month} 个月\n"
        f"发电方案：{event.data.order.plan_title}\n"
    )

    if sku_list := event.data.order.sku_detail:
        sku_text = "\n购买内容："
        for sku in sku_list:
            sku_text += f"\n\t{sku.name} * {sku.count}"
        notice_text += sku_text

    logger.info(notice_text)

    for group_id, user_id in config.afd_token_dict.items():
        if bot.bot_info.user_id == user_id:
            await bot.send_group_msg(group_id=group_id, message=notice_text)
            logger.info(f"已向群 {group_id} 发送本订单的通知")
    raise FinishedException
