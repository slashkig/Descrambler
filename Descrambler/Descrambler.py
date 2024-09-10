import enchant
import sys

def generateWord(ind):
    substring = choices[ind:wordLen]
    if choices[ind] == max(substring):
        if ind == 0: return False
        else: return generateWord(ind - 1)
    else:
        substring.sort()
        choices[ind] = substring.pop(substring.index(choices[ind]) + 1)
        for num in substring:
            ind += 1
            choices[ind] = num
    return True

def addWord(numSet):
    newWord = ""
    for ind in numSet:
        newWord += letterbox[ind]
    sys.stdout.write("\033[F")
    print("Testing: " + newWord)
    return newWord

def checkWord(check):
    suggestions = book.suggest(check)
    weight = len(suggestions)
    for s in suggestions:
        if not matchword(s): continue
        if s not in options: options[s] = 0
        if len(s) == wordLen:
            if sorted(list(s)) == letterbox:
                if s not in solutions: solutions.append(s)
                options[s] += weight * 100
            else: options[s] += weight * 10
        else: options[s] += weight
        weight -= 1

def matchword(match):
    for letter in list(match):
        if letter not in letterbox: return False
    return True

book = enchant.Dict("en_US")

letters = input("Enter word to unscramble: ")
letterbox = list(letters)
letterbox.sort()

word = "".join(letterbox)
wordLen = len(letterbox)
options = dict()
solutions = list()
choices = [i for i in range(wordLen)]

print("Finding possible solutions for '" + letters + "'...")
print(word)

# Generate options
while True:
    checkWord(word)
    if not generateWord(wordLen - 2): break
    word = addWord(choices)

# Results
if len(options) > 0:
    print("\nSolutions found!")
else:
    print("\nNo solutions found.")

if len(solutions) > 0:
    print("Direct solutions: " + ", ".join(solutions), end="\n\n")

# Print options in order of relevance
ceil = sum(options.values())
while len(options) > 0:
    highest = max(options.values())
    for o in list(options.keys()):
        if options[o] == highest:
            print(o + " - " + str(round(highest / ceil * 100, 2)), end="%\n")
            options.pop(o)
print("")

input()