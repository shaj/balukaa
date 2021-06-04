from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import TodoEntry
from .todos_list import todos
from balukaa.nav_main_list import MENU


class TodoJournalListView(LoginRequiredMixin, ListView):
    model = TodoEntry
    template_name = 'todo/todos_journal.html'
    # context_object_name = 'todos'

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        todos =     список задач, пока берется из обычного списка выше в этом файле
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        cart_text = текст info-cart, вызываемой в случае отсутствия записей
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список задач'
        context['todos'] = todos             # get_worked_menu_list
        context['btn_text'] = 'Главная'
        context['btn_href'] = '\\'
        context['cart_text'] = 'В журнале нет дел!'
        context['menu_list'] = MENU
        return context
