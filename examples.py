import random as r
from nltk import edit_distance #Расстояние Левинштейна, мера того, насколько строки отличаются
import re

#text = "Gjdkgn !! !  !"
#text = text.strip()


def filter_text(text):
    text = text
    text = text.lower()
    print(text)
    #Убирать разные символы
    text = text.strip()
    print(text)
    #Найти все знаки преминания и заменить их на пустоту
    expression = r'[^\w\s]'
    text = re.sub(expression, "", text)
    print(text)
    #lambda t: re.sub(r'[^\w\s]', t.lower(), t.strip(),t) уточнить
    return text


print(filter_text("ПРВИЕТ! ! ! !"))
