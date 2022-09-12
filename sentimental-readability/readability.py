from cs50 import get_string
import math

# initialise the variables needed
numberOfSentences = 0
numberOfWords = 0
numberOfLetters = 0
numberOfSpaces = 0
numberOfPunc = 0

text_to_analyse = get_string("Text: ")

# step through the text one character at a time
for i in range(len(text_to_analyse)):
    if text_to_analyse[i] == " ":
        numberOfSpaces += 1
        numberOfWords += 1
    elif text_to_analyse[i] in ("?", "!", "."):
        numberOfPunc += 1
        numberOfSentences += 1
    else:
        numberOfLetters += 1

# catch the last word that is not followed by space
numberOfWords += 1

# use for debugging
#print("Number of letters: " + str(numberOfLetters))
#print("Number of spaces: " + str(numberOfSpaces))
#print("Number of words: " + str(numberOfWords))
#print("Number of sentences: " + str(numberOfSentences))

# L is the average number of letters per 100 words in the text. Using 1.00 to force to float
L = ((numberOfLetters * 1.00) / (numberOfWords)) * 100

# S is the average number of sentences per 100 words in the text. Using 1.00 to force to float
S = ((numberOfSentences * 1.00) / (numberOfWords)) * 100

# final calculation
result = (0.0588 * L) - (0.296 * S) - 15.8
# print(result)
result = math.floor(result)
# print(result)

if result < 1:
    print("Before Grade 1")
elif result > 16:
    print("Grade 16+")
else:
    print("Grade " + str(result))