# bot
Система распознавания лиц по фотографиям с телеграма или любого источника и хранение в базу данных какая личность сколько раз отсканировалась (любая БД)
  а) telegram bot
  б) база данных
  в) система распознавания лиц
  
Используемые библиотеки:
- telebot
- onnx (библиотека эффективно реализует широкий спектр современных алгоритмов распознавания/детектирования/выравнивания лиц, необходимый компонент для insightface)
- insightface (библиотека для facerecognition) 
- onnxruntime (для предсказания на CPU для onnx)

Источники:
- https://pypi.org/project/pyTelegramBotAPI/ (telebot)
- https://habr.com/ru/articles/773744/ (insightface)
- https://habr.com/ru/articles/754400/ (sqlite3)
