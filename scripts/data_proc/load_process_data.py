import random as r
from nltk import edit_distance #Расстояние Левинштейна, мера того, насколько строки отличаются
import json
import re
import pandas as pd


with open("bot/big_bot_config.json", "r") as config_file:
    data = json.load(config_file)
    
INTENTS = data['intents']
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
    if distance > 3:
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
            if text_match(user_text, example):
                return intent
    
#print(get_intent("ПРВИЕТ ! ! !"))

#print(get_intent("привет"))
# СДелать случайный ответ из карты намерений
def get_random_response(intent):
    return r.choice(INTENTS[intent]['responses'])
  
# Классификация текстов
filter_text(text.input())
