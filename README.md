# Face recognition Telegram Bot
Система распознавания лиц по фотографиям с телеграма или любого источника и хранение в базу данных какая личность сколько раз отсканировалась (любая БД)
  а) telegram bot
  б) база данных
  в) система распознавания лиц
  
## Используемые библиотеки:
- telebot
- onnx (библиотека эффективно реализует широкий спектр современных алгоритмов распознавания/детектирования/выравнивания лиц, необходимый компонент для insightface)
- insightface (библиотека для facerecognition) 
- onnxruntime (для предсказания на CPU для onnx)

## Источники:
- https://pypi.org/project/pyTelegramBotAPI/ (telebot)
- https://habr.com/ru/articles/773744/ (insightface)
- https://habr.com/ru/articles/754400/ (sqlite3)

## Демонстрация работы Telegram-бота:
Запустим бота и отправим две фотографии:

<img src="https://github.com/user-attachments/assets/27f3f1a3-736d-4849-8daa-a7c59d5af169" height="500">

Как мы видим, данного человека еще не было в базе данных.

Теперь добавим еще одну фотографию:

<img src="https://github.com/user-attachments/assets/a3426d95-0c17-40d3-a351-e795ba78dd4b" height="500">

Бот отвечает, что данный человек уже встречался один раз.

Проверим с другим человеком:

<img src="https://github.com/user-attachments/assets/bc7e1af6-d7db-44cf-a8b7-6681d9527d44" height="500">

<img src="https://github.com/user-attachments/assets/140c1444-f5b5-4926-9d3c-370d19788f0a" height="500">

Как мы можем видеть, бот работает корректно.
