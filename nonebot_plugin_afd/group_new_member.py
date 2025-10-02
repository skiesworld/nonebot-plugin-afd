import asyncio
import random

import nonebot
from nonebot import get_bot, logger, on_request
from nonebot.adapters.afdian import TokenBot
from nonebot.adapters.afdian.exception import ActionFailed
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupRequestEvent

from .config import plugin_config


def group_rule(event: GroupRequestEvent) -> bool:
    """
    处理规则，只允许配置内的群号来处理
    :param event: GroupRequestEvent
    :return: 是否同意
    """
    return event.group_id in set(plugin_config.afd_token_dict.keys())


new_member = on_request(rule=group_rule)


@new_member.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    logger.debug(f"用户 {event.user_id} 请求加入群聊 {event.group_id}")
    if not event.comment:
        logger.debug(f"用户 {event.user_id} 未填写答案，已忽略")
        return

    comment = event.comment.strip()

    if event.sub_type != "add":
        logger.debug(f"用户 {event.user_id} 的请求类型为 {event.sub_type}，已忽略")
        return

    # if "\n答案：" not in comment:
    #     logger.debug(f"用户 {event.user_id} 的答案不符合自定义答案格式，已忽略")
    #     return

    # comment = comment[comment.find("\n答案：") + 4:]
    logger.debug(f"用户 {event.user_id} 的订单号为 {comment}")

    if not (author_user_id_list := plugin_config.afd_token_dict.get(event.group_id)):
        logger.warning(f"未找到群聊 {event.group_id} 的作者 user_id 配置，已忽略")
        return

    logger.info(f"本群已配置的作者 user_id 有：{author_user_id_list}")

    logger.info(nonebot.get_bots())

    # 遍历本群所有作者的user_id
    logger.debug(
        f"开始遍历群聊 {event.group_id} 的作者 user_id 列表 {author_user_id_list}"
    )

    for user_id in author_user_id_list:
        logger.info(f"正在尝试获取作者 {user_id} 的 Bot")
        try:
            afdian_bot = get_bot(user_id)
            logger.info("获取 Bot 成功")
        except Exception:
            logger.warning(
                f"群聊 {event.group_id} 的 AFDianBot {user_id} 不存在，将尝试获取下一个 AFDianBot"
            )
            continue

        if not isinstance(afdian_bot, TokenBot):
            logger.warning(f"Bot {user_id} 不是爱发电 TokenBot，继续寻找")
            continue

        logger.debug(
            f"已经找到群聊 {event.group_id}，作者 {user_id} 的爱发电Bot，开始查询订单"
        )

        try:
            order_response = await afdian_bot.query_order_by_out_trade_no(
                out_trade_no=comment
            )
        except ActionFailed as e:
            logger.error(
                f"查询用户 {event.user_id} 的订单 {comment} 出现异常，也可能该订单不属于当前Bot，将继续使用下一个作者的 user_id 进行查询，错误信息为：{e}"
            )
            continue

        logger.debug(order_response)

        if order_response.ec != 200:
            logger.error(
                f"查询用户 {event.user_id} 的订单 {comment} 失败，错误信息为：{order_response.em}"
            )
            logger.debug("已尝试使用下一个作者的 user_id 进行查询")
            continue
        logger.debug(f"查询用户 {event.user_id} 的订单 {comment} 成功")

        if not order_response.data.list:
            msg = f"检测到用户 {event.user_id} 的订单号已存在，但数据列表为空，忽略此事件，需要作者 {user_id[:5]}{'x' * 8} 自行处理"
            logger.debug(msg)
            await bot.send_group_msg(group_id=event.group_id, message=msg)
            logger.debug(f"已将用户 {event.user_id} 通知发送至群聊 {event.group_id}")
            return

        delay = random.uniform(3, 5)
        logger.debug(
            f"用户 {event.user_id} 的订单号 {comment} 数据列表不为空，将在 {delay:.2f} 秒后同意请求"
        )
        await asyncio.sleep(delay)
        await event.approve(bot)
        logger.debug(
            f"用户 {event.user_id}，使用订单号 {comment}，加入群聊 {event.group_id}"
        )
        return

    else:
        msg = f"用户 {event.user_id} 的订单号 {comment[:5]} 不属于群聊 {event.group_id} 的任何作者，已拒绝请求"
        logger.warning(msg)
        await bot.send_group_msg(group_id=event.group_id, message=msg)
        await event.reject(bot, reason="订单号不属于群聊的作者")
