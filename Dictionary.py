import csv
import requests
import os.path
import datetime
dict_stat_path = 'dict_stats.csv'
dict_stat_exist = True if os.path.exists(dict_stat_path) else False
def get_word_from_api(source_word: str) -> tuple or None:
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
    return definition, example, part_of_speach
def read_stats(dict_stat_path: str)-> dict:
    stats_dict = {}
    word_for_stats = ''
    if os.path.exists(dict_stat_path):
        with open(dict_stat_path, 'r') as f:
            read = csv.reader(f, delimiter='^')
            next(read)
            for row in read:
                word_for_stats = row[0]
                count_for_stats = row[1]
                add_date_for_stats = row[2]
                stats_dict[word_for_stats] = {'Count': count_for_stats, 'Last': add_date_for_stats}
    return stats_dict
def update_dict_stats(dict_stat_path: str, word: str)->dict:
    time = datetime.datetime.now()
    last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
    stats = read_stats(dict_stat_path)
    if word in stats.keys():
        print("Last search", stats[word]['Last'])
        stats[word]['Count'] = str(int(stats[word]['Count']) + 1)
        stats[word]['Last'] = last
    else:
        stats[word] = {'Count': '1', 'Last': last}
    return stats
def save_stats(dict_stat_path: str, stats: dict) -> None:
    with open(dict_stat_path, 'w') as f:
        header = 'Word^Count^Last\n'
        f.write(header)
        for key, value in stats.items():
            row = key + "^" + value["Count"] + "^" + value["Last"] + "\n"
            f.write(row)
def create_dict_file(dict_path: str, first_data: str)-> True:
    now = datetime.datetime.now()
    last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
    row = first_data + "^" + last + "\n"
    with open(dict_path, 'w') as f:
        header = "Word^Part_of_Speach^Definition^Example^add_Date\n"
        f.write(header)
        f.write(row)
    return True
def append_dict(dict_path: str, word_info: str)-> True:
    now = datetime.datetime.now()
    last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
    row = word_info + "^" + last + "\n"
    with open(dict_path, 'a') as f:
        f.write(row)
    return True
def pd_from_file(file_name: str)-> dict:
    data = {}
    with open(file_name, 'r') as f:
        dict_file = csv.reader(f, delimiter= '^')
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
def print_info(word: str, part_of_speach: str, definition: str, example: str, add_date: str)-> None:
    print(f'Word - {word},'
          f' PoS - {part_of_speach},'
          f' Definition - {definition},'
          f' Example - {example},', end='')
    if add_date:
        print(f' Date - {add_date}')