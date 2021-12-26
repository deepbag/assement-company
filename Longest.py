import sys
import timeit

# Starting Time 
timeStart = timeit.default_timer()

# Define Node
class TrieNode:
    def __init__(self, letter=None, ending=False):
        self.letter = letter
        self.ending = ending # Ending Point False
        self.children = {} # Creating empty Dictionary

# Define Trie
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def strInsertion(self, word):
        curr_node = self.root
        for letter in word:
            if letter not in curr_node.children:
                curr_node.children[letter] = TrieNode(letter)
            curr_node = curr_node.children[letter]
        curr_node.ending = True

    def __contains__(self, word):
        curr_node = self.root
        for letter in word:
            if letter not in curr_node.children:
                return False
            curr_node = curr_node.children[letter]
        return curr_node.ending

    # Check Words Can Make More Words
    def checkPrefix(self, word):
        # If False Need to Start Traversing The Trie
        curr_node = self.root
        for index, letter in enumerate(word):
            if letter not in curr_node.children:
                return 0, []
            curr_node = curr_node.children[letter]
            if curr_node.ending:
                suffix = word[index + 1:]                           
                suffix_count, suffix_list = self.checkPrefix(suffix)    
                if suffix_count:                                   
                    return 1 + suffix_count, [word[:index + 1]] + suffix_list 
        return curr_node.ending, [word]

    def getCompound(self, word):
        checkPrefix_num, checkPrefix_list = self.checkPrefix(word)
        return checkPrefix_num > 1, checkPrefix_num, checkPrefix_list

def loadFile(filename):
    words = []
    trie = Trie()
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip()
            trie.strInsertion(word)
            words.append(word)
    return trie, words

def processList(compoundWords):
    compoundWords.sort(key=lambda x: len(x[0]), reverse=True)
    return compoundWords

def getCompound(trie, words):
    compound = []
    for word in words:
        isValid, num, dlist = trie.getCompound(word)
        if isValid:
            compound.append((word, num, dlist))
    return compound

def printLongestWord(filename):
    trie, words = loadFile(filename)
    compoundWords = processList(getCompound(trie, words))

    # Prints Longest Compound Word
    longestWord = compoundWords[0][0]
    secondLongestWord = compoundWords[1][0]

    print(f"Longest Compound Word: {longestWord}")
    print(f"Longest Compound Word: {secondLongestWord}")

    return trie, words, compoundWords

if __name__ == "__main__":
    wordList = sys.argv[1]
    printLongestWord(wordList)

    # Stop Time and Print Time
    timeStop = timeit.default_timer()
    takenTime = timeStop - timeStart
    print(f"Time Taken: {takenTime}")