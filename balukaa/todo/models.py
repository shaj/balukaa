from django.db import models
from django.utils.translation import gettext_lazy as _
from .services import work_up_string


class TodoEntry(models.Model):
    """ Записи журнала "Список дел"

    Для удобства date_range - CharField, а не DateField
    Идеальная точность для списка дел не важна, а для истории можно свободно записывать дату любых форматах:
    - "01.06.2021";
    - "июн.2021";
    - "май-июн.2021"
    - "25.мая-7.июн.2021"
    """
    class Statuses(models.IntegerChoices):
        """ Два состояния активности бухгалтерских проводок

        Отсюда:
        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
        """
        ENABLE = 1, _('В работе')
        DISABLE = 0, _('Сделано')

    date_range = models.CharField(max_length=64, default="")
    task = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    status = models.IntegerField(
        choices=Statuses.choices,
        default=Statuses.ENABLE,
    )
    comment = models.CharField(max_length=256)
    creator = models.CharField(max_length=32)

    def __str__(self):
        return "%s, %s" % \
               (self.task,
                self.date_range)

    def get_description(self):
        return '%s, %s, %s, %s, %s, %s' % \
               (self.date_range,
                self.task,
                self.description,
                self.get_status(),
                self.comment,
                self.creator)

    def get_absolute_url(self):
        pass

    def get_status(self):
        return self.Statuses(self.status).label

    def date_range_map(self):
        return work_up_string(self.date_range)

    def task_map(self):
        return work_up_string(self.task)

    def description_map(self):
        return work_up_string(self.description)

    def status_map(self):
        return work_up_string(self.get_status())

    def comment_map(self):
        return work_up_string(self.comment)

    def creator_map(self):
        return work_up_string(self.creator)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
