# medium | stegano-crypto | book

## Название

Book

## Описание

> В былые времена один философ написал трактат о жизни и бренности всего сущего. Есть информация, что в этом тексте спрятан флаг. Сможете найти?
> 
> _Формат флага: `Sabantuy{...}`._

## Деплой

Деплой не требуется.

## Файлы

Участникам нужно выдать содержимое папки [public/](public/).

## Решение

Невооружённым глазом заметно, что в выданном файле `book.txt` часть пробелов — одиночные, а часть — двойные. Можно предположить, что это какая-то битовая кодировка: один из разделителей кодирует бит `1`, другой разделитель — бит `0`. Перебрав два варианта, мы достаём из текста бинарные данные:

```
b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03\xed\x96[\x8f\xa36\x14\x80\xe79\xbf\xc2\xab>\x00jJlll\x18)\x95\xb6\xd3U+\xad\xaa\xaev\xd5\xa7\xaaB6\x1c\x12v\x13@\xe0$\x93F\xf9\xef\xb5\x03\x99Mf\xa6\xdb\xa7\xe9E\xf5\'\x11\x13\x9fs|n\x96MY\xad l\xf77/\t6\x08\x11\xdb\x91\x88\x18_\x8e\x96(\xc2\xd1\ra$"<b\xb1\x9d\'\x98\xf3\xe8\x06\xe1\x17\x8djd\xd3k\xd9!t\xb3\xc5[\xf9%\xbd\xbf\x92\xffG\xf9\xea\xd5l\xd3w3U\xd53\xa8\xb7\xa8\xdd\xebeS\xd3\xc9\xa4Z\xb7M\xa7Q\xd3O&e\xd7\xac\xd1]\xb7ou\x13\xfe\xa2\xab\x15\x1ae\xefdQT\xf5\xe2J~W\xb5K\xe8\xce\x1a\xaf\xdf|\xb8\x92\xbe\xdb\xa8U\x95\xbf\x85\xfdY\xe1\xfd\x87\xd7\x93\xc9\xa4\x80\x12I\xe83\xa8s\xab\xe7\x7f\x82\xfd-R{\r\xfd\x14\x15R\xcb\xf1O\x80\xbe\xf9vx\xbb\x9d C\xb5Es\x13`\xb8\xe9d]4k\xdfx\x0b\xd5\xaa\xc9?e}\xf5;\x04\'\x9d|\x88gnC\tk\xd8\xd9\xb5\xe7\xe6\x99\x1a\xeby\xb5\x9d\xa2uS\xc0\xdc\n\x7f\xfa\xf9\xfb7\xd9\xddww\xc1\xe4d\xd8\x81\xdet\xf5h\x1f\x9e#\x1bS\x0e[Y\xf86\xb2)z\xe44\x18\xd3\xe9zy\x9d\x8e\xc94|\xdf\xcb\xb7\xd6\xf5\x17rjW\xb2\xaa5\xdck\x13\xb2y\tm\xf5\xb2\x93|\xf4\xe7\xa9j\xe1]\xe66*\xb7\xcd\xce\x7f0\x9e"\xe33\x84a\xa8\x9f\xcb\xc8j\x85\xba\x19\x97\xf6/&U\xa5\xb3\x15\xd4\x0b\xbd\xf4\x03\xf45\x12\x01\x9a\xcdP\xf2\xe0xHom\x1c\xf9\xc1\x10\xb2\xed\x9c\xf1\xf3\xb4\x17f\xf2T\x94_\xf1oC\xc0\xb6(\x83\xa6\xad\xc6\x02j\xe8\xa4\x06\xdfx\xec\xe7\x04Gl\x8a`N\xc7hw\x95^\xa2\xa6\x85\xda\xf7\xca\x95\\\x84\xfa^{&\x88\xce\x0b\x90\xecQiN\xad\xc1\xbb\xc5*\x98E\xedd\xd8\x81iM\x10\xf6\xba\xabZ\x7f\\k,Q\xe9\xfd\xd04\x05\xfa\xd8\xa8W\xe8G\xe8\x00U=\xda7\x9b\xeed\x7f\x8b\x0ev8z\xb6\xd7fO\x9cm\xc7&B\x91\x8d\xab\\n\xd41\xf5\xe9\xc9C\xf0H\xffs].7\xc3X\x83\xe9\xb9l\xa3\x9bF}4\x8a\x87\x87\x94\xbck\xbf\xde\xed\xa3@\xc2%\xdc\xfb\xc1\xf49\xfdq\xe1+\x93qn\xb0:\x19\x1d\x9f\x94\xb9\xd9\xe8v\xa3\xcf\x85\xde=[h[\xe1]W\x99\xa6\x95\xde\xc1\xc4|<\x98\x9e\xaf\xaa\x1azh\x8f\xde\xd5F3;\xa5*Q\x96\xd5r\rY\x86\xe6s\xe4e\x99\xdd7Y\xe6\r+\x0e\x9bh\xf2O\x9f\x80\xffo>w\xfd\xe5|\xd8K\x9es\xf6g\xf7?f\x1c\x9f\xee\xff\x88P\xca\x191\xf7?a\x02\xbb\xfb\xff\xef\xe0\xf0\xf4\xa4\xf1\x94\x90<\xc1\x82\xaaD\xca\x88\x8b<I#\xcaT\nQ\x0e\xdct)!2\x06\xce"\x11\xb3$\xa2q\x89\xcd\xc8\x13\x02*J\x8cE\xca8M\xb1H%f\xb1\x11S(\x0bF\x8a(\x95\x10Q\xc10c%\xc7\xd4\xe8\xc7D%9\xd0\x94\x16`\x94\x14Oi\xaa\x88"\t\xa5\x89\x80"\xe6\x94J,YIH,\x94J\x84*\x94\xcc\xf3B\x94XH{>=w\xdeyI\x024g\x00q\xce\x84 ,/K\xf3M\x89)Os\x19\x9b\x0c8\xa72.Dl\xc2c\t\xc3\x92\xa6\x117\xbfqJr\x95b\xa0\x98%\xb8\x90\xa4`\x89\x8aXJ1\xcd\x85\xc8i\x94c\x01B\x99\xafT\xec\x1d\xddi\xe5p8\x1c\x0e\x87\xc3\xe1p8\x1c\x0e\x87\xc3\xe1p8\x1c\x0e\x87\xc3\xe1p8\xfe\xb5\xfc\x01\xd9H\xc8\xa6\x00(\x00\x00'
```

По сигнатуре (или с помощью различных утилит, таких как `file`) можно понять, что это — сжатые алгоритмом `gzip` данные. После расжатия оказывается, что внутри данных содержится `tar`-архив, то есть, фактически, это был архив в формате `.tar.gz`. Внутри этого архива лежат два файла:

- `file.py` — скрипт на языке Python
- `output.txt` — вывод этого скрипта

Код скрипта ([dev/file.py](dev/file.py)) шифрует сообщение с флагом алгоритмом [AES-128-CBC](https://ru.wikipedia.org/wiki/AES_(%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82_%D1%88%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)), используя случайно сгенерированные ключ `aes_key` и IV. При этом, само сообщение выглядит так:

```python
f'Good job! Here is your flag: {flag}'
```

Использованный ключ для AES затем шифруется алгоритмом [RSA](https://ru.wikipedia.org/wiki/RSA) со случайно сгенерированным ключом `rsa_key`. В итоге содержимое `output.txt` имеет вид:

```python
{
    'encrypted_text': 'b7a6...f07a',
    'encrypted_aes_key': '88e3...2200'
}
```

Нам не выдаётся закрытый ключ RSA, соответственно, мы не можем расшифровать `aes_key`. Кроме этого, нам не выдаётся и _открытый_ ключ RSA, то есть мы не знаем даже модуль `N`! Как в этой ситуации можно взломать шифр?

Нужно заметить, что в параметрах RSA используется 1024-битный модуль и публичная экспонента `e = 3`. Ключ для AES имеет длину 128 бит, соответственно, шифртекст будет иметь длину 128 * 3 = 384 бита. Это сильно меньше, чем размер модуля, значит, мы сможем "расшифровать" `aes_key`, просто взяв от него корень третьей степени:

```
aes_key ^ 3 == encrypted_aes_key (mod N)

N ~ 1024 bit
aes_key ~ 128 bit  =>  encrypted_aes_key ~ 384 bit

aes_key ^ 3 == encrypted_aes_key
aes_key == cube_root(encrypted_aes_key)
```

Отлично, мы получили ключ для AES. Но осталась одна проблема: используемый в шифровании режим — [CBC](https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%B6%D0%B8%D0%BC_%D1%81%D1%86%D0%B5%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_%D0%B1%D0%BB%D0%BE%D0%BA%D0%BE%D0%B2_%D1%88%D0%B8%D1%84%D1%80%D0%BE%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%B0) (режим сцепки блоков). Для корректной расшифровки он требует вектор инициализации — IV, который нам не выдали.

К счастью, первый блок (16 байт) сообщения не содержит флаг: `b'Good job! Here i'`. Используя свойство режима CBC, мы можем заменить IV на <u>первый</u> блок шифртекста, а расшифровку начать <u>со второго</u> блока. Мы получим неполное сообщение, но зато в нём будет флаг:

```python
b's your flag: Sabantuy{a8c2d1966c160bb6d289024015253c05}'
```

Пример решения: [dev/solution.py](dev/solution.py)

## Флаг

```
Sabantuy{a8c2d1966c160bb6d289024015253c05}
```
