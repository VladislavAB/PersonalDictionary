from Dictionary_object import Dictionary
import os
import csv
import random
import datetime


# print(f'Dict: {game.pd}\nGame stat: {game.game_stat}\nDict stat: {game.dict_stat}')
class Game:
    def __init__(self):
        self.dict_path = 'dict.csv'
        self.dict_stat_path = 'dict_stats.csv'
        self.game_stat_path = 'game_stats.csv'
        self.game_stat_exist = True if os.path.exists(self.game_stat_path) else False

        self.dictionary = Dictionary(self.dict_path, self.dict_stat_path)
        self.pd = self.dictionary.__pd_from_file__(self.dict_path)
        self.dict_stat = self.dictionary.read_dict_stat()
        self.sorted_dict_stat = self.read_sorted_dict_stat()

        self.game_stat = self.read_game_stat()
        self.sorted_game_stat = self.read_sorted_game_stat()

    def read_sorted_dict_stat(self) -> list:
        dict_stats_list = []
        if os.path.exists(self.dict_stat_path):
            with open(self.dict_stat_path, 'r') as f:
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

    def read_game_stat(self) -> dict:
        game_stats_dict = {}
        if os.path.exists(self.game_stat_path):
            with open(self.game_stat_path, 'r') as f:
                read = csv.reader(f, delimiter='^')
                next(read)
                for row in read:
                    word = row[0]
                    wrong_answers = row[1]
                    right_answers = row[2]
                    last = row[3]
                    game_stats_dict[word] = {'wrong': int(wrong_answers), 'right': int(right_answers), 'last': last}
        return game_stats_dict

    def read_sorted_game_stat(self) -> list:
        read_game_stat = self.game_stat
        sorted_game_statistic = []
        if read_game_stat:
            for key, value in read_game_stat.items():
                sorted_game_statistic.append([key, value['wrong']])
            sorted_game_statistic.sort(key=lambda x: x[1], reverse=True)
            sorted_game_statistic = [i[0] for i in sorted_game_statistic]
            return sorted_game_statistic
        else:
            return sorted_game_statistic

    def game_number(self) -> int:
        game_stat_exist = True if os.path.exists(self.game_stat_path) else False
        game_number_ = None
        if len(self.pd.keys()) >= 10 and game_stat_exist is False:
            game_number_ = 1
        elif len(self.sorted_game_stat) == 5:
            game_number_ = 2
        elif len(self.game_stat.keys()) >= 10:
            game_number_ = 3
        return game_number_

    def get_num_from_source(self, source: list, exclude: list, count: int) -> list:
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

    def change_elements(self, source: list, elements: list) -> list:
        count = len(elements)
        while count > 0:
            for word_to_change in elements:
                source.pop(0)
                source.append(word_to_change)
                count -= 1
        return source

    def create_words(self, game_number: int) -> list:
        pack = []
        if game_number == 1:
            pack = list(self.pd.keys())[:5]
            random.shuffle(pack)
        elif game_number == 2:
            pack = list(self.pd.keys())[5:10]
            random.shuffle(pack)
        else:
            while len(pack) < 5:
                word = list(self.pd.keys())[random.randint(0, len(self.pd) - 1)]
                if word not in pack:
                    pack.append(word)
        unique_words_game = self.get_num_from_source(self.sorted_game_stat, pack, 2)
        pack = self.change_elements(pack, unique_words_game)
        unique_words_dict = self.get_num_from_source(self.sorted_dict_stat, pack, 1)
        pack = self.change_elements(pack, unique_words_dict)
        return pack

    def get_answers(self, word: str) -> list:
        answers = []
        pd_definitions = []
        answers.append(self.pd[word]['definition'])  # Add right answer
        for word, description in self.pd.items():
            pd_definitions.append(description["definition"])
        while len(answers) != 4:
            num = random.randint(0, len(self.pd) - 1)
            if pd_definitions[num] not in answers:
                answers.append(pd_definitions[num])
        random.shuffle(answers)
        return answers

    def input_guess(self, word) -> int:
        guess_OK = False
        guess = None
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

    def play_game(self, pack: list):
        wrong_answers = []
        right_answers = []
        question_number = 1
        for word in pack:
            answers = self.get_answers(word)
            print(f'Вопрос № {question_number}')
            for index in range(len(answers)):
                print(f'{index + 1}.{answers[index]}')
            question_number += 1
            print('-----------')
            guess = self.input_guess(word)
            if self.pd[word]['definition'] == answers[int(guess) - 1]:
                right_answers.append(word)
                print('Правильный ответ!')
            else:
                wrong_answers.append(word)
                print('Неправильный ответ!')
        return right_answers, wrong_answers

    def make_current_game_stat(self, right_answers: list, wrong_answers: list) -> dict:
        time = datetime.datetime.now()
        last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
        game_stat = {}
        for word in right_answers:
            game_stat[word] = {'right': 1, 'wrong': 0, 'last': last}
        for word in wrong_answers:
            game_stat[word] = {'wrong': 1, 'right': 0, 'last': last}
        return game_stat

    def update_dict_stats(self, current_game_stat: dict) -> dict:
        time = datetime.datetime.now()
        last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
        for word in current_game_stat.keys():
            if word in self.game_stat.keys():
                self.game_stat[word]['wrong'] = self.game_stat[word]['wrong'] + current_game_stat[word]['wrong']
                self.game_stat[word]['right'] = self.game_stat[word]['right'] + current_game_stat[word]['right']
                self.game_stat[word]['last'] = last
            else:
                self.game_stat[word] = {'wrong': current_game_stat[word]['wrong'],
                                        'right': current_game_stat[word]['right'],
                                        'last': current_game_stat[word]['last']}
        return self.game_stat

    def create_game_stats(self, current_game_stat: dict) -> True:
        now = datetime.datetime.now()
        last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
        with open(self.game_stat_path, 'w') as f:
            header = "Word^Wrong^Right^last_Date\n"
            f.write(header)
            for word, stat in current_game_stat.items():
                row = word + "^" + str(stat['wrong']) + "^" + str(stat['right']) + "^" + last + "\n"
                f.write(row)
        return True

    def save_game_stats(self, updated_stats: dict) -> True:
        with open(self.game_stat_path, 'w') as f:
            header = "Word^Wrong^Right^last_Date\n"
            f.write(header)
            for key, value in updated_stats.items():
                row = key + "^" + str(value['wrong']) + "^" + str(value['right']) + "^" + value['last'] + "\n"
                f.write(row)
        return True


game = Game()
game_number = game.game_number()
pack = game.create_words(game_number)
right_answers, wrong_answers = game.play_game(pack)
current_game_stat = game.make_current_game_stat(right_answers, wrong_answers)
if game.game_stat_exist:
    updated_stats = game.update_dict_stats(current_game_stat)
    game.save_game_stats(updated_stats)
else:
    game.create_game_stats(current_game_stat)
