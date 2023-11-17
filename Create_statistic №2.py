# СТАТИСТИКА №2 количество вводов слова в строку (поиска), дата последнего поиска.
# 1. Создается файл при вводе слова, если слово уже существует со столбцами Word^Count_of_inputs^Date_of_last_input
# 2. В переменную count_of_inputs добавляется единица, изначально count_of_inputs = 0 и идет в столбец Date_of_last_input
# 3. Формируется переменная date_of_last_input, актуальная дата и идет в столбец Date_of_last_input
# 4. Берется word, который ввели и идет в столбец Word.
# 5. После первого ввода выводится статистика.
# 6. На второй ввод переменная count_of_inputs увеличивается на 1 и date_of_last_input перезаписывается.
import csv
header = 'Word^Count_of_inputs^Date_of_last_input'
with open('dict_stats.csv', 'w') as f:
    stats_file = csv.writer(f, delimiter='^')
print(stats_file)

row = word + '^' + count_of_inputs + '^' + date_of_last_input + '\n'
with open('dict_stats.csv', 'a') as f:
    f.write(header)
    f.write(row)
    print(f)