from Dictionary_object import Dictionary

dictionary = Dictionary('dict.csv', 'dict_stats.csv')

word = dictionary.word_input()
word_info = dictionary.get_word_info(word)
if not dictionary.in_dictionary(word):
    print(
        f"Word : {word_info.split('^')[0]}\nPart of speach: {word_info.split('^')[1]}\nDescription: {word_info.split('^')[2]}\nExample: {word_info.split('^')[3]}")
    dictionary.add_to_dictionary(word)
    dictionary.save_to_file(word_info)
else:
    dictionary.update_dict_stats(word)
    dictionary.save_dict_stats()
