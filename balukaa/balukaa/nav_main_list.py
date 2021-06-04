from django.urls import reverse_lazy

MENU = [
    # Группа меню: Справочники
    {
        'item_group': 'Справочники',
        'item_text': 'План счетов',
        'item_url': reverse_lazy('ledger:accounts_book')
    },
    # Группа меню: Журналы
    {
        'item_group': 'Журналы',
        'item_text': 'Журнал проводок',
        'item_url': reverse_lazy('ledger:entries_journal')
    },
    # Группа меню: Отчеты
    {
        'item_group': 'Отчеты',
        'item_text': 'Движения по журналу проводок',
        'item_url': reverse_lazy('ledger:movements_report')
    },
    {
        'item_group': 'Отчеты',
        'item_text': 'Карточка счета',
        'item_url': reverse_lazy('ledger:account_card_report', args=['50'])
    },
    {
        'item_group': 'Отчеты',
        'item_text': 'Баланс',
        'item_url': reverse_lazy('ledger:account_balance_report')
    },
    # Группа меню: Разное
    {
        'item_group': 'Разное',
        'item_text': 'Панель администратора',
        'item_url': '/admin/'
    },
    {
        'item_group': 'Разное',
        'item_text': 'Список дел',
        'item_url': reverse_lazy('todo:todos_journal')
    },
    {
        'item_group': 'Разное',
        'item_text': 'О нас',
        'item_url': reverse_lazy('about')
    },
]
