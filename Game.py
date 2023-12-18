import random
import os
import Dictionary
import datetime
import csv


# def input_count() -> int:
#     word_OK = False
#     count = None
#     while not word_OK:
#         count = input('Введите количество слов: ')
#         if count.isdigit():
#             count = int(count)
#             if 0 < count <= max_count:
#                 word_OK = True
#             else:
#                 print('Введите цифру в пределах диапазона!')
#         else:
#             print('Вы ввели букву вместо цифры!')
#     return count


# Делает проверку на ввод, диапазон количества слов.
def get_words_from_dict(count: int) -> list:
    words = []
    pd_words = list(pd.keys())  # Лист всех слов
    if count <= len(pd_words):
        while len(words) != count:
            number = random.randint(0, len(pd) - 1)
            if pd_words[number] not in words:
                words.append(pd_words[number])
    else:
        words = pd_words
    return words


# Возвращает список рандомных слов равное count или меньше, все слова, которые есть.
def input_guess() -> int:
    guess_OK = False
    guess = None
    question_number = 1
    while not guess_OK:
        guess = input(f'Что означает слово: {word}? ')
        if guess.isdigit():
            guess = int(guess)
            if 0 < guess <= 4:
                guess_OK = True
            else:
                print('Введите цифру в пределах диапазона!')
        else:
            print('Вы ввели букву вместо цифры!')
    return guess


# Делает проверку на ввод, диапазон выбора слова.
def make_current_game_stat(right_answers: list, wrong_answers: list) -> dict:
    time = datetime.datetime.now()
    last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
    game_stat = {}
    for word in right_answers:
        game_stat[word] = {'right': 1, 'wrong': 0, 'last': last}
    for word in wrong_answers:
        game_stat[word] = {'wrong': 1, 'right': 0, 'last': last}
    return game_stat


# Делает статистику из первой игры. После - обнуляется.
def create_game_stats(current_game_stat: dict) -> True:
    now = datetime.datetime.now()
    last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
    with open(game_stat_path, 'w') as f:
        header = "Word^Wrong^Right^last_Date\n"
        f.write(header)
        for word, stat in current_game_stat.items():
            row = word + "^" + str(stat['wrong']) + "^" + str(stat['right']) + "^" + last + "\n"
            f.write(row)
    return True


# Создает файл csv из первой статистики.
def read_game_stats() -> dict:
    game_stats_dict = {}
    if os.path.exists(game_stat_path):
        with open(game_stat_path, 'r') as f:
            read = csv.reader(f, delimiter='^')
            next(read)
            for row in read:
                word = row[0]
                wrong_answers = row[1]
                right_answers = row[2]
                last = row[3]
                game_stats_dict[word] = {'wrong': int(wrong_answers), 'right': int(right_answers), 'last': last}
    return game_stats_dict


def read_sorted_game_stat() -> list:
    read_game_stat = read_game_stats()
    sorted_game_statistic = []
    if read_game_stat:
        for key, value in read_game_stat.items():
            sorted_game_statistic.append([key, value['wrong']])
        sorted_game_statistic.sort(key=lambda x: x[1], reverse=True)
        sorted_game_statistic = [i[0] for i in sorted_game_statistic]
        return sorted_game_statistic
    else:
        return sorted_game_statistic


def read_dict_statistic() -> list:
    dict_stats_list = []
    if os.path.exists(dict_stat_path):
        with open(dict_stat_path, 'r') as f:
            read = csv.reader(f, delimiter='^')
            next(read)
            for row in read:
                word = row[0]
                count = row[1]
                last = row[2]
                dict_stats_list.append([word, int(count)])
            dict_stats_list.sort(key=lambda x: x[1], reverse=True)
            dict_stats_list = [i[0] for i in dict_stats_list]
    return dict_stats_list


def update_dict_stats(read_stats: dict, current_game_stat: dict) -> dict:
    time = datetime.datetime.now()
    last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
    for word in current_game_stat.keys():
        if word in read_stats.keys():
            read_stats[word]['wrong'] = read_stats[word]['wrong'] + current_game_stat[word]['wrong']
            read_stats[word]['right'] = read_stats[word]['right'] + current_game_stat[word]['right']
            read_stats[word]['last'] = last
        else:
            read_stats[word] = {'wrong': current_game_stat[word]['wrong'], 'right': current_game_stat[word]['right'],
                                'last': current_game_stat[word]['last']}
    return read_stats


def save_game_stats(updated_stats: dict) -> True:
    with open(game_stat_path, 'w') as f:
        header = "Word^Wrong^Right^last_Date\n"
        f.write(header)
        for key, value in updated_stats.items():
            row = key + "^" + str(value['wrong']) + "^" + str(value['right']) + "^" + value['last'] + "\n"
            f.write(row)
    return True


def get_answers(word: str) -> list:
    answers = []
    pd_definitions = []
    answers.append(pd[word]['definition'])  # Add right answer
    for word, description in pd.items():
        pd_definitions.append(description["definition"])
    while len(answers) != 4:
        num = random.randint(0, len(pd) - 1)
        if pd_definitions[num] not in answers:
            answers.append(pd_definitions[num])
    random.shuffle(answers)
    return answers


# Возвращает список рандомных определений равное 4, включая правильное определение.
def get_num_from_source(source: list, exclude: list, count: int) -> list:
    result = []
    uniq_from_source = set(source) - set(exclude)
    diff_len = len(uniq_from_source)
    if diff_len >= 0:
        count = min(diff_len, count)
        while count > 0:
            word_to_add = source.pop(0)
            if word_to_add not in exclude:
                result.append(word_to_add)
                count -= 1
    return result


def change_elements(source: list, elements: list) -> list:
    count = len(elements)
    while count > 0:
        for word_to_change in elements:
            source.pop(0)
            source.append(word_to_change)
            count -= 1
    return source


pd = {}
dict_path = 'dict.csv'
dict_stat_path = 'dict_stats.csv'
game_stat_path = 'game_stats.csv'
max_count = 5
dict_exist = True if os.path.exists(dict_path) else False
dict_stat_exist = True if os.path.exists(dict_stat_path) else False
game_stat_exist = True if os.path.exists(game_stat_path) else False

pd = Dictionary.pd_from_file(dict_path)

game_stats = read_game_stats()
sorted_game_statistic = read_sorted_game_stat()
dict_stats = read_dict_statistic()
check_count_words = len(read_game_stats().keys())

# Определение игры
game_number = None
if len(pd.keys()) >= 10 and game_stat_exist is False:
    game_number = 1
elif len(sorted_game_statistic) == 5:
    game_number = 2
elif check_count_words >= 10:
    game_number = 3
# _________________
pack = []
# create words for play
if game_number == 1:
    pack = list(pd.keys())[:5]
    random.shuffle(pack)
elif game_number == 2:
    pack = list(pd.keys())[5:10]
    random.shuffle(pack)
else:  # game number > 2
    while len(pack) < 5:
        word = list(pd.keys())[random.randint(0, len(pd) - 1)]
        if word not in pack:
            pack.append(word)
    unique_words_game = get_num_from_source(sorted_game_statistic, pack, 2)
    pack = change_elements(pack, unique_words_game)
    unique_words_dict = get_num_from_source(dict_stats, pack, 1)
    pack = change_elements(pack, unique_words_dict)

# Game start
wrong_answers = []
right_answers = []

# Игра
question_number = 1
for word in pack:
    answers = get_answers(word)  # Возвращает список рандомных определений равное 4, включая правильное определение.
    print(f'Вопрос № {question_number}')
    for index in range(len(answers)):
        print(f'{index + 1}.{answers[index]}')
    question_number += 1
    print('-----------')
    guess = input_guess()
    if pd[word]['definition'] == answers[int(guess) - 1]:
        right_answers.append(word)
        print('Правильный ответ!')
    else:
        wrong_answers.append(word)
        print('Неправильный ответ!')

current_game_stat = make_current_game_stat(right_answers, wrong_answers)
if game_stat_exist:
    read_game_stat = read_game_stats()
    updated_stats = update_dict_stats(read_game_stat, current_game_stat)
    save_game_stats(updated_stats)
else:
    create_game_stats(current_game_stat)
