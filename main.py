import sys

from src.connections import bot
from src.helpers import datetime_arg, get_chat
from src.mention import all_members, recent_active, search


async def run(args):
    print(args.__dict__)
    try:
        async with bot:
            chat = await get_chat(args.chat)

            if args.func == 'all':
                await all_members(bot, chat, schedule_date=args.schedule_datetime)

            elif args.func == 'recent':
                await recent_active(bot, chat, schedule_date=args.schedule_datetime)

            elif args.func == 'search':
                print('Обмеження Telegram: пошук за запитом застосовується лише до супергруп і каналів.')
                await search(bot, chat, schedule_date=args.schedule_datetime, query=args.query)

    except ValueError as err:
        print('Error:', err)
        sys.exit()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='Mention')
    subparsers = parser.add_subparsers(help='Відмітити учасників чату:', dest='func')

    parser_a = subparsers.add_parser('all', help='Усіх', formatter_class=argparse.RawTextHelpFormatter)
    parser_a.add_argument('--chat', '-с', action='store', required=True, type=str, help='Юзернейм, посилання або ID чату')
    parser_a.add_argument('--schedule_datetime', '-dt', action='store', type=datetime_arg,
                          help='Дата та час для запланованого відправлення.\nПриклад:\n90s\tвідправлення через 90 з поточного часу\n10m\tвідправлення через 10 хв\n"29-09-2024 18:00"\tвідправленя за вказаною датою та часом')

    parser_b = subparsers.add_parser('recent', help='Нещодавно активних', formatter_class=argparse.RawTextHelpFormatter)
    parser_b.add_argument('--chat', '-с', action='store', required=True, type=str, help='Юзернейм, посилання або ID чату')
    parser_b.add_argument('--schedule_datetime', '-dt', action='store', type=datetime_arg,
                          help='Дата та час для запланованого відправлення.\nПриклад:\n90s\tвідправлення через 90 з поточного часу\n10m\tвідправлення через 10 хв\n"29-09-2024 18:00"\tвідправленя за вказаною датою та часом')

    parser_c = subparsers.add_parser('search', help='За ключовим словом в імені / юзернеймі', formatter_class=argparse.RawTextHelpFormatter)
    parser_c.add_argument('--chat', '-с', action='store', required=True, type=str, help='Юзернейм, посилання або ID чату')
    parser_c.add_argument('--query', '-q', action='store', required=True, type=str, help='Запит для пошуку')
    parser_c.add_argument('--schedule_datetime', '-dt', action='store', type=datetime_arg,
                          help='Дата та час для запланованого відправлення.\nПриклад:\n90s\tвідправлення через 90 з поточного часу\n10m\tвідправлення через 10 хв\n"29-09-2024 18:00"\tвідправленя за вказаною датою та часом')

    args = parser.parse_args()
    bot.run(run(args))
