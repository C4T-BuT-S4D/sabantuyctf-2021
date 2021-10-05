# easy | crypto | simple-cipher

## Название

Simple cipher

## Описание

> Злоумышленник проник к нам в систему и зашифровал флаг. К счастью, нам удалось раздобыть код алгоритма шифрования. Зная его, попробуйте восстановить данные.
> 
> _Зашифрованный флаг находится в файле `output.txt`. Формат флага: `Sabantuy{...}`._

## Деплой

Деплой не требуется.

## Файлы

Участникам нужно выдать содержимое папки [public/](public/).

## Решение

Рассмотрим функцию `encrypt()`:

```python
def encrypt(key: bytes, plaintext: bytes) -> bytes:
    ciphertext = []

    for i in range(len(plaintext)):
        byte = plaintext[i]

        for j in range(len(key)):
            byte = ((byte ^ i) ^ (key[j] + j)) ^ (i * j)

        ciphertext.append(byte & 0xFF)

    return bytes(ciphertext)
```

Она работает так: каждый байт `plaintext` ксорится с каким-то числом — значением выражения, которое зависит от байтов ключа и индексов.

Для удобства перепишем шифрование байта, используя свойства операции XOR:

```python
byte = byte ^ (key[j] + j) ^ (i ^ (i * j))
```

Можно заметить, что выражение `(i ^ (i * j))` мы можем посчитать заранее, так как знаем значения нужных индексов. Кроме этого, выражение `(key[j] + j)` принимает одинаковые значения для всех байтов `plaintext`. Следовательно, мы можем перебрать все возможные значения выражения `(key[j] + j)` и обратить шифрование, используя обратимость операции XOR.

Среди полученных 256 возможных флагов нужно выбрать тот, который содержит только печатаемые символы и начинается с `Sabantuy{`.

Пример решения: [dev/solution.py](dev/solution.py)

## Флаг

```
Sabantuy{3b863fdbc7c8f827d27d83a623bbae28}
```