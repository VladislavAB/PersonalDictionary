import random
import os
import Dictionary

def get_words_from_dict(count):
    words = []
    pd_words = list(pd.keys()) #Лист всех слов
    while len(words) != count:
        number = random.randint(0, len(pd)-1)
        if pd_words[number] not in words:
            words.append(pd_words[number])
    return words
# Возвращает список рандомных слов равное count.
def get_answers(word):
    answers = []
    pd_definitions = []
    answers.append(pd[word]['definition'])  # Add right answer

    for word, description in pd.items():
        pd_definitions.append(description["definition"])
    while len(answers) != 4:
        num = random.randint(0, len(pd)-1)
        if pd_definitions[num] not in answers:
            answers.append(pd_definitions[num])
    random.shuffle(answers)
    return answers
# Возвращает список рандомных определений равное 4, включая правильное определение.

pd = {}
dict_path = 'dict.csv'
dict_stat_path = 'stats.csv'
dict_exist = True if os.path.exists(dict_path) else False
dict_stat_exist = True if os.path.exists(dict_stat_path) else False
pd = Dictionary.pd_from_file(dict_path)

count = int(input('Введите количество слов: '))

words = get_words_from_dict(count)# Возвращает список рандомных слов равное count.

for word in words:
    answers = get_answers(word)# Возвращает список рандомных определений равное 4, включая правильное определение.
    for index in range(len(answers)):
        print(f'{index+1}.{answers[index]}')
    guess = int(input(f'Что означает слово: {word}? '))
    if pd[word]['definition'] == answers[int(guess)-1]:
        print('Вы угадали!')
        # update Statistic #1
    # К файлу статистики применить метод sorted, создать топ худших слов.
    else:
        print('Вы не угадали')
        # update Statistic #1