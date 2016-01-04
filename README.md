# pricedog
Набор скриптов позволяющий отслеживать стоимость товаров.

На данный момент поддерживаются следующие магазины:
* e2e4online (http://e2e4online.ru)
* dns (http://dns-shop.ru)

Настройки программы и собранная информация хранятся в файле
базы данных SQLite: **$HOME/.config/pricedog/pricedog.db**

## Зависимости
* python (>= 2.7)

## Использование
```bash
=== pricedog control v0.1.0 ===
Usage:
    pricedog_ctl.py <command> <arg1> ... <argN>
Command details:
    init                       -- init the database
    shop list                  -- show the shop list
    task add <shop> <link>     -- add the new task
    task remove <shop> <link>  -- remove the task
    task list                  -- show the task list 
    price list <shop> <link> [<step_in_days>]  -- show price list
    price_machine list <shop> <link> [<step_in_days>]  -- machine redable pricelist
```

Инициализация базы данных(следует сделать до начала использования программы):
```bash
pricedog_ctrl.py init
```

Добавление нового товара в список отслеживания стоимости:
```bash
pricedog_ctrl.py task add shop_name http://link_to_the_item/
```

Запуск сбора информации о стоимости товаров находящихся в списке отслеживания:
```bash
pricedog_execute.py
```

Запуск pricedog_execute.py можно прописать в cron:
```bash
# Запускать скрипт ежедневно в 23:00
00 23 * * * /path/to/script/pricedog_execute.py
# Запустить скрипт через 600 секунд после включения компьютера
@reboot sleep 600 ; /path/to/script/pricedog_execute.py
```
