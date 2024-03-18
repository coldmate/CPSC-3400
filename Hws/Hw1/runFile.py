from collections import deque
def hw1():
    words = []

    for line in open("words.txt"):
        if len(line) < 8:
            words.append(line)

    for line in open("pairs.txt"):
        if not line.split():
            break
        x, y = line.split()
        queue = deque()
        queue.append(x)
        a = set(x)
        b = set(y)

        print()
        
        '''
        print({a for a in x if a not in y})
        print({a for a in y if a not in x})
        print()
        '''
        
        print("** Looking for ladder from %s to %s" % (x, y))
        
        if len(x) != len(y):
                print("%s and %s are not the same length" % (x, y), end="")
        else:
            print("The ladder is: ", end="")
            for word in queue:
                print("%s -> " % (word), end="")
        print()
