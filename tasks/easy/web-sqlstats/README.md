# easy | web | Shops Site 

## Название

Shops Site

## Описание

> Наш знакомый фрилансер просит проверить кусочек его работы: сайта для интернет магазина с несколькими пунктами выдачи. 
>
> Он даже любезно оставил флаг в базе данных, но говорит что получить его невозможно.  
> 
> _Формат флага: `Sabantuy{[A-Za-z0-9_]+}`._
## Деплой
`cd deploy && docker-compose up --build -d`

## Файлы

Участникам нужно выдать ссылку на приложение, порт = 40000.

## Решение

Просто SQL-injection в которой все **пробелы удаляются** (видно по запросу при ошибке). 

Для решения достаточно заменить пробелы на табы или `/**/`, затем с помощью UNION-инъекции найти вторую таблицу и вытащить из нее единственную строчку.

## Флаг

```
Sabantuy{SqlInj3ction_1s_e4sy_b4t_cr1t1c4l}
```