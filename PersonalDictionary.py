import csv
import requests
import os.path
import datetime
def get_word_from_api(source_word):
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
def create_stats(first_word):
    header = 'Word^Count^Last\n'
    count = 1
    time = datetime.datetime.now()
    last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
    row = first_word + '^' + str(count) + '^' + last + '\n'
    with open(dict_stat_path, 'w') as file:
        file.write(header)
        file.write(row)
    print(' '.join(row.split('^')))
    return True
def read_stats():
    stats_dict = {}
    word_for_stats = ''
    with open(dict_stat_path, 'r') as f:
        read = csv.reader(f, delimiter='^')
        next(read)
        for row in read:
            word_for_stats = row[0]
            count_for_stats = row[1]
            add_date_for_stats = row[2]
            stats_dict[word_for_stats] = {'Count': count_for_stats, 'Last': add_date_for_stats}
    return stats_dict
def update_dict_stats(word):
    time = datetime.datetime.now()
    last = time.strftime('%d') + '|' + time.strftime('%b') + '|' + time.strftime('%y')
    stats = read_stats()
    if word in stats.keys():
        stats[word]['Count'] = str(int(stats[word]['Count']) + 1)
        stats[word]['Last'] = last
    else:
        stats[word] = {'Count': '1', 'Last': last}
    print(stats)
    return stats
def save_stats(stats):
    with open(dict_stat_path, 'w') as f:
        header = 'Word^Count^Last\n'
        f.write(header)
        for key, value in stats.items():
            row = key + "^" + value["Count"] + "^" + value["Last"] + "\n"
            f.write(row)
def create_dict(first_data):
    now = datetime.datetime.now()
    last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
    row = first_data + "^" + last + "\n"
    with open(dict_path, 'w') as f:
        header = "Word^Part_of_Speach^Definition^Example^add_Date\n"
        f.write(header)
        f.write(row)
    return True
def append_dict(word_info):
    now = datetime.datetime.now()
    last = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
    row = word_info + "^" + last + "\n"
    with open(dict_path, 'a') as f:
        f.write(row)
    return True
def pd_from_file(file_name):
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
def from_dict(word):
    now = datetime.datetime.now()
    add_date = now.strftime('%d') + '|' + now.strftime('%b') + '|' + now.strftime('%y')
    part_of_speach = pd[word]["part_of_speach"]
    definition = pd[word]["definition"]
    example = pd[word]["example"]
    return part_of_speach, definition, example, add_date
def print_info(word, part_of_speach, definition, example, add_date):
    print(f'Word - {word},'
          f' PoS - {part_of_speach},'
          f' Definition - {definition},'
          f' Example - {example},', end='')
    if add_date:
        print(f' Date - {add_date}')

pd = {}
dict_path = 'dict.csv'
dict_exist = True if os.path.exists(dict_path) else False
dict_stat_path = 'stats.csv'
dict_stat_exist = True if os.path.exists(dict_stat_path) else False

word = input('Введите слово: ')

if dict_exist:
    pd = pd_from_file(dict_path)
    if word in pd.keys():
        part_of_speach, definition, example, add_date = pd[word]["part_of_speach"], pd[word]["definition"], pd[word]["example"], pd[word]["add_Date"]
        print_info(word, part_of_speach, definition, example, add_date)
        if dict_stat_exist:
            stats = update_dict_stats(word)
            save_stats(stats)
        else:
            create_stats(word)
        exit()
else:
    api_response = get_word_from_api(word)
    if api_response:
        definition, example, part_of_speach = api_response
        print_info(word, part_of_speach, definition, example, None)
        word_info = word + '^' + part_of_speach + '^' + definition + '^' + example
        if dict_exist:
            append_dict(word_info)
        else:
            create_dict(word_info)
    else:
        print("No Definitions Found")
        exit()
