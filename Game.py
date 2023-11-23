import random
import os
import Dictionary

pd = {}
dict_path = 'dict.csv'
dict_exist = True if os.path.exists(dict_path) else False
dict_stat_path = 'stats.csv'
dict_stat_exist = True if os.path.exists(dict_stat_path) else False
pd = Dictionary.pd_from_file(dict_path)

count = int(input('Введите количество слов: '))

pd_list = []
for key, value in pd.items():
    pd_list.append(key)

words = []
while len(words) != count//2:
    number = random.randint(0, len(pd)-1)
    print(number)
    if pd_list[number] not in words:
        words.append(pd_list[number])
print(words)
