import random
import os
import Dictionary
import datetime
import csv
def make_current_game_stat(right_answers, wrong_answers):
    time = datetime.datetime.now()
    last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
    game_stat = {}
    for word in right_answers:
        game_stat[word] = {'right': 1, 'wrong': 0, 'last': last}
    for word in wrong_answers:
        game_stat[word] = {'wrong': 1, 'right': 0, 'last': last}
    return game_stat
def create_game_stats(current_game_stat):
    now = datetime.datetime.now()
    last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
    with open(game_stat_path, 'w') as f:
        header = "Word^Wrong_Answer^Right_Answer^last_Date\n"
        f.write(header)
        for word, stat in current_game_stat.items():
            row = word + "^" + str(stat['wrong']) + "^" + str(stat['right']) + "^" + last + "\n"
            f.write(row)
    return True
def read_game_stats():
    game_stats_dict = {}
    with open(game_stat_path, 'r') as f:
        read = csv.reader(f, delimiter= '^')
        next(read)
        for row in read:
            word = row[0]
            wrong_answers = row[1]
            right_answers = row[2]
            last = row[3]
            game_stats_dict[word] = {'wrong': int(wrong_answers), 'right': int(right_answers), 'last': last}
    return game_stats_dict
def update_dict_stats(stats, current_game_stat):
    time = datetime.datetime.now()
    last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
    if word in stats.keys():
        stats[word]['wrong'] = stats[word]['wrong'] + current_game_stat[word]['wrong']
        stats[word]['right'] = stats[word]['right'] + current_game_stat[word]['right']
        stats[word]['last'] = last
    else:
        stats[word] = {'wrong': current_game_stat[word]['wrong'], 'right': current_game_stat[word]['right'], 'last': current_game_stat[word]['last']}
    return stats
def save_game_stats(stats):
    with open(game_stat_path, 'w') as f:
        header = "Word^Wrong_Answer^Right_Answer^last_Date\n"
        f.write(header)
        for key, value in stats.items():
            row = key + "^" + str(value['wrong']) + "^" + str(value['right']) + value['last'] + "\n"
            f.write(row)
    return True
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
game_stat_path = 'game_stats.csv'
dict_exist = True if os.path.exists(dict_path) else False
dict_stat_exist = True if os.path.exists(dict_stat_path) else False
game_stat_exist = True if os.path.exists(game_stat_path) else False
pd = Dictionary.pd_from_file(dict_path)

count = int(input('Введите количество слов: '))

words = get_words_from_dict(count)# Возвращает список рандомных слов равное count.
wrong_answers = []
right_answers = []

for word in words:
    answers = get_answers(word)# Возвращает список рандомных определений равное 4, включая правильное определение.
    for index in range(len(answers)):
        print(f'{index+1}.{answers[index]}')
    guess = int(input(f'Что означает слово: {word}? '))
    if pd[word]['definition'] == answers[int(guess)-1]:
        right_answers.append(word)
        print('Вы угадали!')
    else:
        wrong_answers.append(word)
        print('Вы не угадали')


current_game_stat = make_current_game_stat(right_answers, wrong_answers)
if game_stat_exist:
    stats = read_game_stats()
    stats = update_dict_stats(stats, current_game_stat)
    save_game_stats(stats)
else:
    create_game_stats(current_game_stat)



