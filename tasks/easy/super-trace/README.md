# easy | forensics | super trace

## Название

Super Trace

## Описание

> Мы хотели просто напечатать вам флаг на экран нашим скриптом. Но скрипт мы потеряли, осталась только траса его запуска. 
> 
> Может быть вы сможете сами найти флаг?
> 
> _Формат флага: `Sabantuy{...}`._

## Деплой

Деплой не требуется.

## Файлы

Участникам нужно выдать содержимое папки [public/](public/).

## Решение

Участникам дан вывод утилиты `strace` которая логировала все системные вызовы при запуске некоторого python-скрипта.

Внутри лога много мусора, но можно найти момент начала печати флага по характерному системному вызову `write(1, "S\n", 2)`

Далее можно запарсить всё с помощью скрипта или найти руками.

Пример решения: [dev/solution.py](dev/solution.py)

## Флаг

```
Sabantuy{Y0u_s33m_t0_b3_l00k1ng_f0r_th1s_r1ght?}
```