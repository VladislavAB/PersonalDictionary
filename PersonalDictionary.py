import csv
import requests
import os.path
import datetime
import Dictionary

pd = {}
dict_path = 'dict.csv'
dict_exist = True if os.path.exists(dict_path) else False
dict_stat_path = 'dict_stats.csv'
dict_stat_exist = True if os.path.exists(dict_stat_path) else False

word = input('Введите слово: ')

if dict_exist:
    pd = Dictionary.pd_from_file(dict_path)
if word in pd.keys():
    part_of_speach, definition, example, add_date = pd[word]["part_of_speach"], pd[word]["definition"], pd[word]["example"], pd[word]["add_Date"]
    Dictionary.print_info(word, part_of_speach, definition, example, add_date)
    stats = Dictionary.update_dict_stats(dict_stat_path, word)
    Dictionary.save_stats(dict_stat_path, stats)
    exit()
else:
    api_response = Dictionary.get_word_from_api(word)
    if api_response:
        definition, example, part_of_speach = api_response
        Dictionary.print_info(word, part_of_speach, definition, example, None)
        word_info = word + '^' + part_of_speach + '^' + definition + '^' + example
    else:
        print("No Definitions Found")
        exit()
    if dict_exist:
        Dictionary.append_dict(dict_path, word_info)
    else:
        Dictionary.create_dict_file(dict_path, word_info)

