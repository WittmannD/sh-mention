from datetime import datetime
from typing import AsyncIterable, Optional

from pyrogram import Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Chat, ChatMember

from src.helpers import create_user_tag_array, send_tags


async def mention(client: Client, chat: Chat, members: AsyncIterable[ChatMember],
                  schedule_date: Optional[datetime] = None):
    tags = await create_user_tag_array(members)

    if len(tags) == 0:
        return

    return await send_tags(client, chat, tags, schedule_date=schedule_date)


async def all_members(client: Client, chat: Chat, schedule_date: datetime = None):
    users = client.get_chat_members(chat.id)
    return await mention(client, chat, users, schedule_date)


async def admins(client: Client, chat: Chat, schedule_date: datetime = None):
    users = client.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS)
    return await mention(client, chat, users, schedule_date)


async def recent_active(client: Client, chat: Chat, schedule_date: datetime = None):
    users = client.get_chat_members(chat.id, filter=ChatMembersFilter.RECENT)
    return await mention(client, chat, users, schedule_date)


async def search(client: Client, chat: Chat, query: str, schedule_date: datetime = None):
    users = client.get_chat_members(chat.id, query=query, filter=ChatMembersFilter.SEARCH)
    return await mention(client, chat, users, schedule_date)
