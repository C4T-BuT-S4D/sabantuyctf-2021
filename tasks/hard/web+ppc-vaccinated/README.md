# hard | web | vaccinated

## Название

Vaccinated

## Описание

> Нам дали протестировать прототип современной CRM-системы одной компании, которая позволяет найти сотрудников, которые еще не вакцинированы.
>
> Правда из-за повышенной активности разработчикам пришлось добавить туда анти-DDOS решение. 
> 
> Нам кажется это приложение не очень безопасным, может быть вы сможете получить пароль админа ?
>
> _Формат флага: `Sabantuy{[A-Za-z0-9_]+}`._

## Деплой

`cd deploy && docker-compose up --build -d`

## Файлы

Уччастникам нужно выдать ссылку на приложение, порт = 40004.

## Решение

Каптча представляет собой простой поиск md5 от строки с заданным префиксом, нужно найти хэш, который будет начинаться с 0000 подряд.

После решения каптчи мы попадаем на страницу, где делается ajax-запрос к апи получения сотрудников.

Также на странице в HTML-комментариях можно найти ссылку на исходный код сервера. 

В исходном коде можно найти NO-SQL like инъекцию в базу данных, из-за которой можно делать различные действия с фильтрацией по паролю.

С помощью `?login=Admin&password[$gt]=Sabantuy` можно посимвольно перебирать пароль. 

## Флаг

```
Sabantuy{R3ally_noSQLBrut3_m4ster}
```
