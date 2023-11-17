import csv
import requests
import os.path
import datetime
x = datetime.datetime.now()
add_date = x.strftime('%d') + '|' + x.strftime('%b') + '|' + x.strftime('%y')

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
    return definition, example, part_of_speach, add_date


pd = {}
path = 'dict.csv'
file_exist = False
if os.path.exists(path):
    with open('dict.csv', 'r') as f:
        dict_file = csv.reader(f, delimiter='^')
        next(dict_file)
        for row in dict_file:
            word = row[0]
            part_of_speach = row[1]
            definition = row[2]
            example = row[3]
            add_date = row[4]
            pd[word] = {'part_of_speach': part_of_speach, 'definition': definition, 'example': example, 'date_of_add' : add_date}
    file_exist = True

word = input('Введите слово: ')

if file_exist:
    if word in pd.keys():
        print(f'Word - {word}, PoS - {part_of_speach}, Definition - {pd[word]["definition"]}, Example - {pd[word]["example"]}, Date - {add_date}')
        exit()

    api_response = get_word_from_api(word)
    if api_response:
        definition, example, part_of_speach, add_date = get_word_from_api(word)
        row = word + '^' + part_of_speach + '^' + definition + '^' + example + '^' + add_date + '\n'
        with open('dict.csv', 'a') as f:
            f.write(row)
        print(f'Word - {word}, PoS - {part_of_speach}, Definition - {definition}, Example - {example}, Date - {add_date}')
    else:
        print("No Definitions Found")
        exit()
else:
    api_response = get_word_from_api(word)
    if api_response:
        definition, example, part_of_speach = get_word_from_api(word)
        row  = word + '^' + part_of_speach + '^' + definition + '^' + example + '^' + add_date + '\n'
        header = 'Word^Part_of_Speach^Definition^Example^Date_of_addition\n'
        with open('dict.csv', 'w') as f:
            f.write(header)
            f.write(row)
        print(f'Word - {word}, PoS - {part_of_speach}, Definition - {definition}, Example - {example}, Date - {add_date}')
    else:
        print("No Definitions Found")


