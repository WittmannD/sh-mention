import asyncio
import re
from datetime import datetime, timedelta
from typing import AsyncIterable, Iterable, Optional, Union

from pyrogram import Client
from pyrogram.enums import ChatType, ParseMode
from pyrogram.errors import UserNotParticipant, UsernameInvalid
from pyrogram.types import Chat, ChatMember, ChatPreview
from pyrogram.types.user_and_chats.user import Link

from src.connections import bot

USERNAME_RE = re.compile(r'@|(?:https?://)?(?:www\.)?(?:telegram\.(?:me|dog)|t\.me)/(@|\+|joinchat/)?')
TG_JOIN_RE = re.compile(r'tg://(join)\?invite=')

VALID_USERNAME_RE = re.compile(r'^[a-z](?:(?!__)\w){1,30}[a-z\d]$', re.IGNORECASE)


def parse_username(username: str):
    """
    Parses the given username or channel access hash, given
    a string, username or URL. Returns a tuple consisting of
    both the stripped, lowercase username and whether it is
    a joinchat/ hash (in which case is not lowercase'd).

    Returns ``(None, False)`` if the ``username`` or link is not valid.
    """
    username = username.strip()
    m = USERNAME_RE.match(username) or TG_JOIN_RE.match(username)
    if m:
        username = username[m.end():]
        is_invite = bool(m.group(1))
        if is_invite:
            return username, True
        else:
            username = username.rstrip('/')

    if VALID_USERNAME_RE.match(username):
        return username.lower(), False
    else:
        return None, False


async def get_chat(chat_id: Union[str, int]):
    try:
        if type(chat_id) == int or (type(chat_id) == str and chat_id.isnumeric()):
            return int(chat_id)

        chat_id, _ = parse_username(chat_id)

        chat = await bot.get_chat(chat_id)

    except (ValueError, UsernameInvalid):
        raise ValueError(f'Не вдалось знайти чат {chat_id}, або він має обмежений доступ')

    if type(chat) == ChatPreview:
        raise ValueError('Бот повинен бути членом чату та мати привілеї для надсилання повідомлень')

    try:
        me_member = await bot.get_chat_member(chat.id, 'me')
        if hasattr(me_member, 'is_member') and me_member.is_member == False:
            raise UserNotParticipant()

    except UserNotParticipant:
        raise ValueError('Бот повинен бути членом чату та мати привілеї для надсилання повідомлень')

    if chat.type == ChatType.PRIVATE or chat.type == ChatType.BOT:
        raise ValueError('Неправильний тип чату')

    return chat


def chunks(lst, n):
    n = max(1, n)
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def create_user_tag_array(members: AsyncIterable[ChatMember]):
    tag_array = []

    async for member in members:
        if member.user.is_bot or member.user.is_deleted:
            continue

        if member.user.username is not None:
            tag_array.append(f'@{member.user.username}')
        else:
            tag_array.append(member.user.mention())

    return tag_array


async def send_tags(client: Client, chat: Chat, tags: list[Link], schedule_date: Optional[datetime] = None):
    for chunk in chunks(tags, 30):
        message = '\t'.join(chunk)
        await client.send_message(chat.id, message, parse_mode=ParseMode.HTML, disable_notification=False,
                                  schedule_date=schedule_date)
        await asyncio.sleep(1)


def datetime_arg(datetime_string: str):
    time_in_sec_re = re.compile(r'^(\d{1,20})s$', re.IGNORECASE)
    time_in_min_re = re.compile(r'^(\d{1,20})m$', re.IGNORECASE)
    time_in_hrs_re = re.compile(r'^(\d{1,20})h$', re.IGNORECASE)

    m = time_in_sec_re.match(datetime_string) or time_in_min_re.match(datetime_string) or time_in_hrs_re.match(
        datetime_string)

    if m:
        unit = datetime_string[-1]
        multiplier = 1 if unit == 's' else 60 if unit == 'm' else 60 * 24

        value = int(m.group(1)) * multiplier
        return datetime.now() + timedelta(seconds=value)

    acceptable_formats = ['%Y-%m-%d %H:%M %z', '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M', '%d-%m-%Y %H:%M %z',
                          '%d-%m-%Y %H:%M', ]

    for frmt in acceptable_formats:
        try:
            return datetime.strptime(datetime_string, frmt)
        except ValueError as err:
            continue

    return datetime.fromisoformat(datetime_string)
