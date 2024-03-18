from collections import deque
import time

def readWordsFile():
    words = set()
    for line in open("words.txt"):
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
    for line in open("pairs.txt"):
        if not line.split():
            break
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
            print("No ladder found from {} to {}".format(start, target))
        print("It took %s seconds" % (t1 - t0))
