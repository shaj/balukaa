
# TODO

- Посмотреть внимательно:
   - [Blazing fast CI with GitHub Actions, Poetry, Black and Pytest](https://medium.com/@vanflymen/blazing-fast-ci-with-github-actions-poetry-black-and-pytest-9e74299dd4a5)
   - [snok/install-poetry@v1.1.4](https://github.com/marketplace/actions/install-poetry-action)
   - [The Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
- Django-filter
   - [django-filter docs](https://django-filter.readthedocs.io/en/stable/guide/install.html)
   - [django-filter github](https://github.com/carltongibson/django-filter)
   - [django-filter mailing list](https://groups.google.com/g/django-filter)

# Материалы

1. Основные вьюшки на базе классов (#29)
   - #29 [00:53:00] - начало классов вьюшек
   - #29 [01:14:00] - форма не привязанная к модели
   - #30 [00:03:00] - продолжаем формы - ModelForm
2. Пользователи и права
   - #30 [01:00:00] - поехали на пользователей
   - #30 [01:08:00] - начнем с регистрации

3. Тестирование #31, #32


# MEM

- [python venv activate](https://gist.github.com/shaj/5915a0d6f4d523c1991da318288ccdaf)
- [Примеры github workflows](https://github.com/AdCombo/flask-combo-jsonapi/tree/master/.github/workflows)
- Вопрос про **толстую модель**, **тонкий view** и **тупые шаблоны**
- [(GitHub-Flavored) Markdown Editor](https://jbt.github.io/markdown-editor/)

## Замечания по проектной работе

1. [дебаг тулбар лучше подключать только в дебаг режиме](https://github.com/shaj/balukaa/blob/OTUS/balukaa/balukaa/urls.py#L31)
2. [все лишние комментарии лучше удалить из проекта](https://github.com/shaj/balukaa/blob/OTUS/balukaa/ledger/admin.py#L5)
3. [и неиспользуемый код тоже :)](https://github.com/shaj/balukaa/blob/OTUS/balukaa/ledger/forms.py#L17)
4. [все методы и функции в пайтоне принято именовать в snake_case](https://github.com/shaj/balukaa/blob/OTUS/balukaa/ledger/models.py#L15)
5. [и переменные тоже](https://github.com/shaj/balukaa/blob/OTUS/balukaa/ledger/models.py#L138)
6. ✓ [лучше не хардкодить урлы, а использовать reverse_lazy](https://github.com/shaj/balukaa/blob/OTUS/balukaa/ledger/views.py#L47)

Общие моменты: 
- Есть flake8. Отлично! На больших проектах будет помогать. Еще можешь посмотреть в сторону https://wemake-python-stylegui.de/en/0.14.0/index.html
- Нет sentry. Маст хэв на проекте
- Есть докер. Круто :)
- Есть тесты. Это хорошо. Очень помогут в будущем!

## Проекты с защиты

[FullREST API - заказ билетов](https://gitlab.com/adventurerka/airline)

[o-evdokimov/security_bot](https://github.com/o-evdokimov/security_bot)
