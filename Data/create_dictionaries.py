
words = open("Other/most_common_words.txt", "r")

word_dict = {}

for word in words:

    word = word.strip()
    if len(word) >= 9:
        word_dict[word] = word


with open("9plusletters.txt", 'w') as file:
    file.write(str(word_dict))

