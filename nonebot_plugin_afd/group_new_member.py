import nonebot
from nonebot import on_request, CommandSession
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupRequestEvent

# 全局黑名单
global_blacklist = set()

# 分群黑名单，键为群组ID，值为黑名单用户集合
group_blacklist = {}

new_member = on_request()

# 添加至分群黑名单命令
@nonebot.on_command("添加黑名单", aliases=("add_blacklist",), only_to_me=False)
async def add_blacklist(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id

    # 检查命令参数
    member_ids = session.get("member_ids", prompt="请输入要添加到黑名单的成员ID，多个成员用空格隔开")

    # 将成员添加至分群黑名单
    if group_id not in group_blacklist:
        group_blacklist[group_id] = set()
    group_blacklist[group_id].update(member_ids)

    await session.send(f"已将成员 {', '.join(member_ids)} 添加至群组 {group_id} 的黑名单。")


@add_blacklist.args_parser
async def _(session: CommandSession):
    stripped_text = session.current_arg_text.strip()
    if stripped_text:
        # 从用户输入中获取要添加至黑名单的成员ID
        session.state["member_ids"] = stripped_text.split()


# 添加至全局黑名单命令
@nonebot.on_command("添加全局黑名单", aliases=("add_global_blacklist",), only_to_me=False)
async def add_global_blacklist(session: CommandSession):
    user_id = session.event.user_id

    # 检查命令参数
    member_ids = session.get("member_ids", prompt="请输入要添加到全局黑名单的成员ID，多个成员用空格隔开")

    # 将成员添加至全局黑名单
    global_blacklist.update(member_ids)

    await session.send(f"已将成员 {', '.join(member_ids)} 添加至全局黑名单。")


@add_global_blacklist.args_parser
async def _(session: CommandSession):
    stripped_text = session.current_arg_text.strip()
    if stripped_text:
        # 从用户输入中获取要添加至全局黑名单的成员ID
        session.state["member_ids"] = stripped_text.split()


@new_member.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    user_id = event.user_id
    group_id = event.group_id

    # 检查全局黑名单
    if user_id in global_blacklist:
        await event.reject(bot, reason="你在全局黑名单中，无法加入任何群组。")
        return

    # 检查分群黑名单
    if group_id in group_blacklist and user_id in group_blacklist[group_id]:
        await event.reject(bot, reason="你在本群的黑名单中，无法加入。")
        return

    # 如果不在黑名单中，同意加群请求
    await event.approve(bot)
