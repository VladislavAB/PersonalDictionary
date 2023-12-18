from Dictionary_object import Dictionary
import os
import csv
import random


# print(f'Dict: {game.pd}\nGame stat: {game.game_stat}\nDict stat: {game.dict_stat}')

class Game:
    def __init__(self):
        self.dict_path = 'dict.csv'
        self.dict_stat_path = 'dict_stats.csv'
        self.game_stat_path = 'game_stats.csv'

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

    def define_game(self) -> int:
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

    def create_words(self) -> list:
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
    def play_game(self):
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
#             guess input продолжить



game = Game()
game_number = game.define_game()
pack = game.create_words()
print(game_number)
