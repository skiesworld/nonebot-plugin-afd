from nonebot.adapters.afdian import OrderNotifyEvent

from .config import plugin_config

user_ids: set[str] = set()
"""所有作者的 user_id 集合"""

afdian_bot_id_to_group_ids: dict[str, set[int]] = {}
"""通过 afdian bot_id 查找群号列表"""


# 初始化全局数据
def init_global_data():
    """
    根据配置初始化 user_ids 和 afdian_bot_id_to_group_ids
    :param afd_token_dict: {group_id: [user_id, ...]}
    """
    user_ids.clear()
    afdian_bot_id_to_group_ids.clear()
    for group_id, user_id_list in plugin_config.afd_token_dict.items():
        for user_id in user_id_list:
            user_ids.add(user_id)

            if not afdian_bot_id_to_group_ids.get(user_id):
                afdian_bot_id_to_group_ids[user_id] = set()
            afdian_bot_id_to_group_ids[user_id].add(group_id)


def get_description(author_id: str, event: OrderNotifyEvent) -> str:
    notice_text = (
        "[爱发电 | 订单通知]\n"
        f"{'=' * 15}\n"
        f"作者：{author_id[:5]}{'*' * 5} 有新的订单\n"
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
    return notice_text
