import os
import csv
import requests
import datetime
from string import ascii_letters
class Dictionary:
    def __init__(self, dict_path: str):
        if os.path.exists(dict_path):
            self.pd = self.__pd_from_file__(dict_path)

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
        return part_of_speach, definition, example,

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

    def in_dictionary(self, word: str) -> bool:
        if word in self.pd.keys():
            return True
        else:
            return False

    def add_to_dictionary(self, word: str) -> bool:
        api_response = self.get_word_from_api(word)
        now = datetime.datetime.now()
        last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
        part_of_speach, definition, example  = api_response
        self.pd[word] = {'part_of_speach': part_of_speach, 'definition': definition, 'example': example, 'add_Date': last}
        return True

dictionary = Dictionary('dict.csv')

## enter word
word = dictionary.word_input()
## check word in dictionary
if not dictionary.in_dictionary(word):
## if not in dictionary add to dictionary
    dictionary.add_to_dictionary(word)
## print dictionary
dictionary.print_info()


