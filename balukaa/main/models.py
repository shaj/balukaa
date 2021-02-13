from django.db import models


# 43:00 - [проведение миграций](https://www.youtube.com/watch?v=6K83dgjkQNw&t=2580s)

class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

