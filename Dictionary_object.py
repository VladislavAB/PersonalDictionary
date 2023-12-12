import os
import csv


class Dictionary:

    def __init__(self, dict_path: str):
        if os.path.exists(dict_path):
            self.pd = self.__pd_from_file__(dict_path)

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
        if word.lower() in self.pd.keys():
            return True
        else:
            return False




dictionary = Dictionary('dict.csv')
