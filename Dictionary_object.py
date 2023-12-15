import os
import csv
import requests
import datetime
from string import ascii_letters
class Dictionary:
    def __init__(self, dict_path: str, dict_stats_path: str):
        self.dict_path = dict_path
        self.dict_stats_path = dict_stats_path
        self.stat = {}
        if os.path.exists(dict_path):
            self.pd = self.__pd_from_file__(dict_path)
        if os.path.exists(dict_stats_path):
            self.stat = self.read_dict_stat()

    def word_input(self) -> str:
        word_status = False
        word_for_check = ''
        while not word_status:
            word_for_check = str(input('Введите слово: '))
            word_status = True
            for i in word_for_check:
                if i in ascii_letters:
                    continue
                else:
                    word_status = False
            if not word_status:
                print('Введите слово правильно!')
        return word_for_check

    def get_word_from_api(self, source_word: str) -> tuple or None:
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + source_word
        response = requests.get(url)
        response_json = response.json()
        # meanings = response_json[0]['meanings']
        part_of_speach = ''
        definition = ''
        example = ''
        found_verb = False
        # word not found in api
        if isinstance(response_json, dict):
            if response_json['title'] == "No Definitions Found":
                return None
        # looking for verb
        for word in response_json:
            meanings = word['meanings']
            for m in meanings:
                if m['partOfSpeech'] == 'verb':
                    part_of_speach = m['partOfSpeech']
                    definition = m['definitions'][0]['definition']
                    if 'example' in m['definitions'][0].keys():
                        example = m['definitions'][0]['example']
                    else:
                        example = ''
                    found_verb = True
        if not found_verb:
            definition = response_json[0]['meanings'][0]['definitions'][0]['definition']
            part_of_speach = response_json[0]['meanings'][0]['partOfSpeech']
            if 'example' in response_json[0]['meanings'][0]['definitions'][0].keys():
                example = response_json[0]['meanings'][0]['definitions'][0]['example']
            else:
                example = ' '
        return part_of_speach, definition, example

    def __pd_from_file__(self, file_name: str) -> dict:
        data = {}
        with open(file_name, 'r') as f:
            dict_file = csv.reader(f, delimiter='^')
            next(dict_file)
            for row in dict_file:
                word_form_file = row[0]
                part_of_speach = row[1]
                definition = row[2]
                example = row[3]
                add_date = row[4]
                data[word_form_file] = {'part_of_speach': part_of_speach,
                                        'definition': definition,
                                        'example': example,
                                        'add_Date': add_date}
        return data

    def in_dictionary(self, word: str) -> bool:
        if word in self.pd.keys():
            return True
        else:
            return False

    def add_to_dictionary(self, word: str) -> bool:
        api_response = self.get_word_from_api(word)
        now = datetime.datetime.now()
        last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
        part_of_speach, definition, example = api_response
        self.pd[word] = {'part_of_speach': part_of_speach, 'definition': definition, 'example': example, 'add_Date': last}
        return True

    def create_dict_file(self, word_info: str) -> bool:
        now = datetime.datetime.now()
        last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
        row = word_info + "^" + last + "\n"
        with open(self.dict_path, 'w') as f:
            header = "Word^Part_of_Speach^Definition^Example^add_Date\n"
            f.write(header)
            f.write(row)
        return True

    def append_dict_file(self, word_info: str) -> bool:
        now = datetime.datetime.now()
        last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
        row = word_info + "^" + last + "\n"
        with open(self.dict_path, 'a') as f:
            f.write(row)
        return True

    def save_to_file(self, word_info) -> bool:
        dict_exist = True if os.path.exists(self.dict_path) else False
        if dict_exist:
            self.append_dict_file(word_info)
        else:
            self.create_dict_file(word_info)
        return True

    def read_dict_stat(self) -> dict:
        stat = {}
        if os.path.exists(self.dict_stats_path):
            with open(self.dict_stats_path, 'r') as f:
                read = csv.reader(f, delimiter='^')
                next(read)
                for row in read:
                    word_for_stats = row[0]
                    count_for_stats = row[1]
                    add_date_for_stats = row[2]
                    stat[word_for_stats] = {'Count': count_for_stats, 'Last': add_date_for_stats}
        return stat

    def update_dict_stats(self) -> bool:
        time = datetime.datetime.now()
        last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
        if word in self.stat.keys():
            print(f"Count: {self.stat[word]['Count']}\nLast search", self.stat[word]['Last'])
            self.stat[word]['Count'] = str(int(self.stat[word]['Count']) + 1)
            self.stat[word]['Last'] = last
        else:
            self.stat[word] = {'Count': '1', 'Last': last}
            print(f"Count: {self.stat[word]['Count']}\nLast search", self.stat[word]['Last'])
        return True

    def save_dict_stats(self) -> None:
        with open(self.dict_stats_path, 'w') as f:
            header = 'Word^Count^Last\n'
            f.write(header)
            if self.stat:
                for key, value in self.stat.items():
                    row = key + "^" + value["Count"] + "^" + value["Last"] + "\n"
                    f.write(row)

    def print_info(self):
        for key in list(self.pd.keys()):
            word_form_file = key
            part_of_speach = self.pd[key]['part_of_speach']
            definition = self.pd[key]['definition']
            example = self.pd[key]['example']
            add_date = self.pd[key]['add_Date']
            print(f'Word - {word_form_file},'
                  f' PoS - {part_of_speach},'
                  f' Definition - {definition},'
                  f' Example - {example},', end='')
            if add_date:
                print(f' Date - {add_date}')

    def get_word_info(self, word: str):
        if dictionary.get_word_from_api(word):
            part_of_speach, definition, example = dictionary.get_word_from_api(word)
            word_info_inner = word + '^' + part_of_speach + '^' + definition + '^' + example
            return word_info_inner
        else:
            print("No Definitions Found!")
            exit()

dictionary = Dictionary('dict.csv', 'dict_stats.csv')

word = dictionary.word_input()
word_info = dictionary.get_word_info(word)
if not dictionary.in_dictionary(word):
    dictionary.add_to_dictionary(word)
    dictionary.save_to_file(word_info)
else:
    dictionary.update_dict_stats()
    dictionary.save_dict_stats()
# dictionary.print_info()


