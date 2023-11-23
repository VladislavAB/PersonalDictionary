import random
import os
import Dictionary

pd = {}
dict_path = 'dict.csv'
dict_stat_path = 'stats.csv'
dict_exist = True if os.path.exists(dict_path) else False
dict_stat_exist = True if os.path.exists(dict_stat_path) else False
pd = Dictionary.pd_from_file(dict_path)

count = int(input('Введите количество слов: '))

pd_list_words = []
pd_dict_definitions = []
for key, value in pd.items():
    pd_list_words.append(key)
    pd_dict_definitions.append(value)

pd_list_definitions = []
for index in range(len(pd_dict_definitions)):
    pd_list_definitions.append(pd_dict_definitions[index]['definition'])
game_dict = {}
words = []
defenitions = []
answers = []
while len(words) != count//2:
    number = random.randint(0, len(pd)-1)
    if pd_list_words[number] not in words:
        words.append(pd_list_words[number])
        defenitions.append(pd_list_definitions[number])
for index in range(0, len(words)):
    game_dict[words[index]] = defenitions[index]

for word in words:
    number = random.randint(0, len(words)-1)
    while len(answers) < 4:
        answers.append(defenitions[words.index(word)])
        answers.append(defenitions[number])
    print(f'1.{answers[0]}, 2.{answers[1]}, 3.{answers[2]}, 4.{answers[3]}')
    choice = int(input(f'Что означает слово {word}? Введите цифру: '))
    if word ==
#         в дикте сравнить
    записать в answers



print(game_dict)

