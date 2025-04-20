from nonebot import logger, on_notice, get_bots
from nonebot.adapters.afdian import Bot, OrderNotifyEvent
from nonebot.adapters.onebot.v11 import Bot as OneBot

from . import config


def afdian_rule(bot: Bot) -> bool:
    for user_ids in config.afd_token_dict.values():
        if bot.self_id in user_ids:
            return True
    return False


order_handler = on_notice()


@order_handler.handle()
async def handle_afdian_order(bot: Bot, event: OrderNotifyEvent):
    logger.info(f"[爱发电 | 通知]有新的订单 {event.get_order().out_trade_no} 来自用户 {event.get_user_id()}")

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

    logger.info("正在寻找可用Bot")
    for group_id, user_id in config.afd_token_dict.items():
        if bot.self_id in user_id:
            for qqbot in get_bots().values():
                logger.info(f"找到群聊 {group_id} 的Bot {qqbot.self_id}")
                if isinstance(qqbot, OneBot):
                    await qqbot.send_group_msg(group_id=group_id, message=notice_text)
                    logger.info(f"已向群 {group_id} 发送本订单的通知")
