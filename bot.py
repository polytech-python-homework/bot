import telebot
from telebot import types
from urllib.request import urlopen
import os
import sqlite3
from insightface.app import FaceAnalysis
import cv2
import pickle
import numpy as np
from tqdm import tqdm

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    rentange_path TEXT NOT NULL,
    embedding TEXT NOT NULL
)
''')

connection.commit()

app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(256,256))

TOKEN = '7901409888:AAFG-QodKrPQwZVi_Ls87eOk3hTrFkR6zBU'

# Создаем экземпляр бота
bot = telebot.TeleBot(token=TOKEN)

print('Бот запущен')

@bot.message_handler(commands=["start"])
def start(message):
    mess = f'Привет. Я могу по фотографии человека сказать, сколько раз я его видел на других фото. Отправь мне фото.'
    bot.send_message(message.chat.id, mess, parse_mode = 'html')


@bot.message_handler(content_types=['photo'])
def photo(message):   
    
    # получаем исходное изображение
    fileID = message.photo[-1].file_id   
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    # сохранение исходного изображения
    fileList = os.listdir('./images')
    imageCount = len(fileList) + 1
    path = f"./images/image{imageCount}.jpg"
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    print(f'Изображение {path} сохранено')

    # сохраняем изображение с прямоугольниками
    rentangle_path = f'./images_r/image{imageCount}.jpg'
    image = cv2.imread(path)
    faces = app.get(image)
    rimg = draw_on(image, faces) 
    cv2.imwrite(rentangle_path, rimg)
    print(f'Изображение {rentangle_path} сохранено')
    
    # получаем все embeddings и вычисляем скалярное происведение
    embeddings = []
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute(f"SELECT id, embedding FROM persons WHERE user_id={message.from_user.id}")
    for row in c.fetchall():
        embeddings.append(row)
    connection.close()

    embedding = faces[0]['embedding']
    # добавляем строку в базу данных
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO persons (user_id, image_path, rentange_path, embedding) VALUES (?, ?, ?, ?)', (message.from_user.id, path, rentangle_path, ' '.join([str(i) for i in embedding])))
    connection.commit()

    count = 0
    numbers = []
    for i, emb in embeddings:
        emb = np.fromstring(emb, dtype=float, sep=' ')
        sk = np.dot(emb, embedding) / (np.linalg.norm(emb) * np.linalg.norm(embedding))
        if sk >= 0.5:
            print(f'Изображение совпадает с {i} со скалярным произведение деленным на нормы {sk}')
            count += 1
            numbers.append(i)

    msg = f'Человек на данном изображении загружался в систему {count} раз'
    bot.send_message(message.chat.id, msg, parse_mode = 'html')


def draw_on(img, faces):
    dimg = img.copy()
    for i in range(len(faces)):
        face = faces[i]
        box = face.bbox.astype(np.int64)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
        if face.kps is not None:
            kps = face.kps.astype(np.int64)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color,
                               2)
        if face.gender is not None and face.age is not None:
                cv2.putText(dimg,'%s,%d'%(face.sex,face.age), (box[0]-1, box[1]-4),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)
    return dimg

bot.infinity_polling()