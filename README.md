Before you start, fill out `.env.example` and rename it to `.env`

Installation:

```shell
cd sh-mention
python3 -m venv venv
source venv/bin/activate
pip install -r -requirements.txt
```

Docs & Examples:

```shell
#    # DOCS:
#    #####################
#
#    usage: Mention [-h] {all,recent,search} ...
#    
#    positional arguments:
#      {all,recent,search}  Відмітити учасників чату:
#        all                Усіх
#        recent             Нещодавно активних
#        search             За ключовим словом в імені / юзернеймі
#    
#    options:
#      -h, --help           show this help message and exit
#    


#    #####################
#    ## Mention all
#    #####################
#
#    Example: 

python main.py all --chat @example_chat -dt "28-09-2023 18:50"

#
#    usage: Mention all [-h] --chat CHAT [--schedule_datetime SCHEDULE_DATETIME]
#    
#    options:
#      -h, --help            show this help message and exit
#      --chat CHAT, -с CHAT  Юзернейм, посилання або ID чату
#      --schedule_datetime SCHEDULE_DATETIME, -dt SCHEDULE_DATETIME
#                            Дата та час для запланованого відправлення.
#                            Приклад:
#                            90s     відправлення через 90 з поточного часу
#                            10m     відправлення через 10 хв
#                            "29-09-2024 18:00"       відправленя за вказаною датою та часом
#    


#    #####################
#    ## Mention recent active users
#    #####################
#
#    Example: 

python main.py recent --chat @example_chat -dt 30m
     
#    usage: Mention recent [-h] --chat CHAT [--schedule_datetime SCHEDULE_DATETIME]
#    
#    options:
#      -h, --help            show this help message and exit
#      --chat CHAT, -с CHAT  Юзернейм, посилання або ID чату
#      --schedule_datetime SCHEDULE_DATETIME, -dt SCHEDULE_DATETIME
#                            Дата та час для запланованого відправлення.
#                            Приклад:
#                            90s     відправлення через 90 з поточного часу
#                            10m     відправлення через 10 хв
#                            "29-09-2024 18:00"       відправленя за вказаною датою та часом
#    
#    #####################
#    ## Mention by keyword
#    #####################
#     
#    Example:

python main.py search -q "Oleksiy" --chat "https://t.me/joinchat/AAAjD4EXp1RDjVZdQ" -dt 1h

#
#    usage: Mention search [-h] --chat CHAT --query QUERY [--schedule_datetime SCHEDULE_DATETIME]
#    
#    options:
#      -h, --help            show this help message and exit
#      --chat CHAT, -с CHAT  Юзернейм, посилання або ID чату
#      --query QUERY, -q QUERY
#                            Запит для пошуку
#      --schedule_datetime SCHEDULE_DATETIME, -dt SCHEDULE_DATETIME
#                            Дата та час для запланованого відправлення.
#                            Приклад:
#                            90s     відправлення через 90 з поточного часу
#                            10m     відправлення через 10 хв
#                            "29-09-2024 18:00"       відправленя за вказаною датою та часом
#
```