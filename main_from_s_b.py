import random as r
from nltk import edit_distance #Расстояние Левинштейна, мера того, насколько строки отличаются
import json
import re
from sklearn.feature_extraction.text import CountVectorizer as cv
from sklearn.feature_extraction.text import TfidfVectorizer as tf
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_curve
from sklearn.metrics import f1_score

with open("big_bot_config.json", "r") as config_file:
    data = json.load(config_file)

INTENTS = data['intents']


#text = input("введите текст: ")

def answ(text):

    if text in ["Привет", "Хеллоу",]:
        return r.choice(["Здарова!","Привет!"])
    elif text in ["пока"]:
        return r.choice(["Пока!","До встречи!"])
    else:
        return "Не понял"


#Составим карты "намерений", которые поддреживает чат-бот
#INTENTS = {
 #   "Hello": {
  #      "examples": ["Привет", "Хеллоу", "Здарова"],
   #     "response": ["Ну привет", "Давно тебя не было", "Хеллоууу"],
    #}
#}


def filter_text(text):
    text = text.lower()
    #text = text.lower().strip()
    #Убирать разные символы
    text = text.strip()
    #Найти все знаки преминания и заменить их на пустоту
    expression = r'[^\w\s]'
    text = re.sub(expression, "", text)
    #lambda t: re.sub(r'[^\w\s]', t.lower(), t.strip(),t) уточнить
    return text



def text_match(user_text, example):
    user_text = filter_text(user_text)
    example = filter_text(example)

    distance = edit_distance(user_text, example)
    avg_len = (len(user_text) + len(example)) / 2
    # Процент опечаток
    ratio = distance / avg_len
    if distance > 2:
        return False

    elif ratio > 0.4:
        return False

    else:
        return True
       #return ratio > 0.4

#print(text_match("Константинопольский!", "Констнтигопольокий"))

#Все намерения из карты
#print(INTENTS.keys())

#Определение намерений пользователя
def get_intent(user_text):
    for intent in INTENTS:
        examples = INTENTS[intent]["examples"]
        #func = [print(examples == filter_text(user_text)) for examples in INTENTS]
        for example in examples:
            text_match(user_text, example)
            # Интент найден
            return intent
    return None
#print(get_intent("ПРВИЕТ ! ! !"))

#print(get_intent("привет"))
# СДелать случайный ответ из карты намерений
def get_random_response(intent):
    return r.choice(INTENTS[intent]['responses'])

# Классификация текстов
"""
1. Подготовить данные. Обучающая выборка, тестовая выборка. (Фраза и намерение)
2. Как по тексту понять намерение?
3. Обучаем модель классификации. Классифицирует по намерениям.
4. Векторизация текстов.
5. Библиотеки. Sklearn.
6. Пробуем разные модели, настройки, подходы.
7. Оценка модели метриками. (Матрица ошибок (заблуждений) - confusion matrix)
8.
"""
# Подготовка данных
X = [] # Фраза (входные данные)
y = [] # Намерение (выходные данные)

for intent in INTENTS:
    examples = INTENTS[intent]['examples']
    for example in examples:
        text = filter_text(example)
        if len(text) < 3:
            continue
        else:
            X.append(text)
            y.append(intent)

# Векторизация текстов. Текст => вектор [0, 2, 5, 10]
# CountVectirizer, sklearn TfidfVectorizer
"""
1. Набора текстов: {"Мама мыла раму",
"Мыла раму мама",
"Раму мыла мама",
}
2. Обучить векторайзер (обучить = изучить тексты)
мама = 1
мыла = 2
раму = 3

3. Векторизация.
"Мама мыла раму" = [1,2,3]
"Мыла раму мама" = [2,3,1]
"Раму мыла мама" = [3,2,1]

"""

# Создаём векторайзер
vectorizer = cv()

# Обучить векторайзер
vectorizer.fit(X)

# Трансформация данных
vecX = vectorizer.transform(X) # сохраняем векторизованные тексты

model = GradientBoostingClassifier() # Настройки
fit_model = model.fit(vecX,y) # Обучение

print(model.predict(vectorizer.transform(['Любимые занятия твои днём']))) # Сделать предсказание (по фразе определить намерение)

# Метрики
# Оценка качества:
y_pred = model.predict(vecX)

print('score_accuracy_score = ', accuracy_score(y, y_pred))
#print('score_r2_score = ', r2_score(y, y_pred, multioutput = '2500'))
print('score_recall_score = ', recall_score(y, y_pred, average = 'micro'))
#print('score_roc_curve = ', roc_curve(y, y_pred))
print('score_f1_score = ', f1_score(y, y_pred, average = 'macro'))

# Определяем намерение с помощью модели:
def get_intent_ml(text):
    vec_text = vectorizer.transform([text])
    pred_intent = model.predict(vec_text)[0]
    # model.predict_proba() < 30% ? => random.choice(faile_phrase) - определение вероятности других ответов
    # []
    return pred_intent

def bot(text):
    intent = get_intent(text)
    if intent:
        return get_random_response(intent)

    intent = get_intent_ml(text)
    return get_random_response(intent)


