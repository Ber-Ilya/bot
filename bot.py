from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command, Text

model = SentenceTransformer('bert-base-nli-mean-tokens')

import sqlite3
from sqlite3 import Error


def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(
            'questions_db.sqlite')  # создаём новую базу данных sqlite3
        print(sqlite3.version)
    except Error as e:
        print(e)

    if conn:
        return conn


def create_table(conn):
    try:
        sql_create_questions_table = """ CREATE TABLE IF NOT EXISTS questions (
                                        id integer PRIMARY KEY,
                                        question text NOT NULL,
                                        name text,
                                        phone text
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_questions_table)
    except Error as e:
        print(e)


conn = create_connection()
if conn is not None:
    create_table(conn)
else:
    print("Error! Cannot create the database connection.")

with open("knowledge_base.json", "r", encoding="utf-8") as file:
    data = json.load(file)

bot_token = '5864216251:AAF-uP6r15oBpkRe3pzorX-jtqlGWeypHuo'
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

qa_pairs = [(q, a) for item in data["намерения"] for q, a in
            zip(item["вопросы"], item["ответы"])]


def encode_questions(questions):
    return np.array(model.encode(questions))


question_embeddings = encode_questions([qa[0] for qa in qa_pairs])


class Form(StatesGroup):
    name = State()
    phone = State()


def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Заявка на проект", "Заявка на согласование", "Задать вопрос"]
    markup.add(*(types.KeyboardButton(text) for text in buttons))
    return markup


@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = get_keyboard()
    await message.answer("Выберите одну из опций:", reply_markup=keyboard)


@dp.message_handler(Text(equals='Заявка на проект'), state='*')
@dp.message_handler(Text(equals='Заявка на проект'), state='*')
async def process_request(message: types.Message, state: FSMContext):
    await state.update_data(request_type='Заявка на проект')
    await Form.name.set()
    await message.answer("Введите ваше имя:")


@dp.message_handler(Text(equals='Заявка на согласование'), state='*')
async def process_request(message: types.Message, state: FSMContext):
    await state.update_data(request_type='Заявка на согласование')
    await Form.name.set()
    await message.answer("Введите ваше имя:")


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Form.next()
    await message.answer("Введите ваш номер телефона:")


@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    await bot.send_message(1991548939,
                           f"Заявка: \nИмя: {user_data['name']}\nТелефон: {message.text}")
    c = conn.cursor()
    c.execute("INSERT INTO questions(name, phone, question) VALUES(?, ?, ?)",
              (user_data['name'], message.text, 'some default value',))
    conn.commit()
    await state.finish()
    await message.answer("Ваша заявка отправлена.")


@dp.message_handler(Text(equals='Задать вопрос'), state='*')
async def answer_question(message: types.Message):
    answer = await get_answer(message.text)
    await message.answer(answer)


@dp.message_handler(state='*', content_types=types.ContentType.TEXT)
async def default_answer(message: types.Message):
    answer = await get_answer(message.text)
    await message.answer(answer)


async def get_answer(input_question, lower_threshold=0.85, upper_threshold=0.93):
    input_question_embedding = encode_questions([input_question])
    similarities = cosine_similarity(input_question_embedding, question_embeddings)[0]
    closest_question_index = np.argmax(similarities)
    c = conn.cursor()
    c.execute("INSERT INTO questions(question) VALUES(?)", (input_question,))
    conn.commit()
    if similarities[closest_question_index] < lower_threshold:
        return "Извините, нет данных, попробуйте переформулировать вопрос."
    elif similarities[closest_question_index] < upper_threshold:
        return f"Извините, вот что я нашёл: {qa_pairs[closest_question_index][1]}"
    else:
        return qa_pairs[closest_question_index][1]


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
    conn.close()
