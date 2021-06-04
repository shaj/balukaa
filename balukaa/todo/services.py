def work_up_string(work_str):
    """ Переводит plain-text в html

    Делает:
    - удаляет пробелы;

    - удаляет начальный символ \\n;
    - заменяет символы \\n на теги </br>

    - заменяет символы </ на &lt;&frasl;
    - заменяет символы < на &lt;
    - заменяет символы > на &gt;
      для того, чтобы в текст можно было свободно писать теги, но они не отображались бы

    - заменяет символы /* на <span class="strong">, //* на </span>,
    - заменяет символы /_ на <span class="incline">, //_ на </span>,
    - заменяет символы /% на <span class="entity">, //% на </span>,
    - заменяет символы /$ на <code>, //$ на </code>,
      для удобного форматирования текста, когда нужно
    """
    work_str = work_str.strip()
    while work_str.startswith('\n'):
        work_str = work_str.replace('\n', '', 1)

    work_str = work_str.replace('</', '&lt;&frasl;')
    work_str = work_str.replace('<', '&lt;')
    work_str = work_str.replace('>', '&gt;')

    work_str = work_str.replace('//*', '</span>')
    work_str = work_str.replace('/*', '<span class="strong">')

    work_str = work_str.replace('//_', '</span>')
    work_str = work_str.replace('/_', '<span class="incline">')

    work_str = work_str.replace('//%', '</span>')
    work_str = work_str.replace('/%', '<span class="entity">')

    work_str = work_str.replace('//$', '</code>')
    work_str = work_str.replace('/$', '<code>')
    return work_str.replace('\n', '</br>')
