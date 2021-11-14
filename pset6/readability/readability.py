# my python code style.


# asking user for an input
user_text = str(input("Text: "))

# using list comprehansion we are splitting user input to individual characters array(list) and then making new array(list) but picking only letters
# and counting them with len
n_letters = len([x for x in list(user_text) if x.isalpha()])

# just splitting user input to words and counting them with len
n_words = len(user_text.split())

# doing the same as on the line 9, but now picking only punctuation and counting with len.
# so we need only count where the sentence ends, that's why.
n_sentences = len([x for x in list(user_text) if x in ".!?"])

# this is ugly long, but I wanted to make as less lines as possible
gradeX = round(0.0588 * ((n_letters / n_words) * 100) - 0.296 * ((n_sentences / n_words) * 100) - 15.8)

# Printing out results.
if gradeX < 1:
    print(f"Before Grade 1")
elif gradeX > 16:
    print(f"Grade 16+")
else:
    print(f"Grade {gradeX}")
