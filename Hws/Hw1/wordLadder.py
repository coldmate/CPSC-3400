from collections import deque
import time

'''
allWords = set() # store the words from words.txt

result = findLadder(start, target)
if result == []:
    print("No ladder fround from {} to {}".format(start, target))
else:
    print("Ther ladder is:", ' -> '.join(result))


first find all adjacent words
put the list in a dictionary
'''

def readWordsFile():
    words = set()
    with open("words.txt") as file:
        for line in file:
            if len(line) < 8:
                words.add(line.strip())
    return words

def findAdjWords(word, setOfWords):
    adjWords = set()
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    for i in range(len(word)):
        for letter in alphabet:
            newWord = word[:i] + letter + word[i + 1:]
            if newWord in setOfWords and newWord != word:
                adjWords.add(newWord)
                
    return adjWords

def findLadder(start, target, setOfWords):
    queue = deque([[start]])
    visited = set()

    while queue:
        ladder = queue.popleft()
        currWord = ladder[-1]
        if currWord == target:
            return ladder

        if currWord not in visited:
            visited.add(currWord)
            adjWords = findAdjWords(currWord, setOfWords)

            for adjWord in adjWords:
                if adjWord not in visited:
                    queue.append(ladder + [adjWord])

    return None

def wordLadder():
    setOfWords = readWordsFile();
    with open("pairs.txt") as file:
        for line in file:
            if not line.split():
                #break
                continue
            start, target = line.split()
        
            print()
            print("** Looking for ladder from %s to %s" % (start, target))
            if len(start) != len(target):
                print("%s and %s are not the same length" % (start, target))
                continue

            t0 = time.time()
            result = findLadder(start, target, setOfWords)
            t1= time.time()
        
            if result:
                print("The ladder is:", ' -> '.join(result))
            else:
                print("No ladder found from %s to %s" % (start, target))
            print("It took %s seconds" % (t1 - t0))
