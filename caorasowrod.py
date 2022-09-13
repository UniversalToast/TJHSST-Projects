import sys, random, time
from heapq import heappush, heappop

begin = time.perf_counter()
hxw = sys.argv[1]
hxw = hxw.split("x")
height = int(hxw[0])
width = int(hxw[1])
size = height * width
allindeces = [i for i in range(size)]
allindeces = set(allindeces)
frequencies = "etaoinsrhldcumfpgwybvkxjqz"
frequencies = frequencies.upper()
board = ""
wordlists = []
wordconnection = dict()  # to see which indexes affect which words
curword = dict()  # keeps track of what each word is
wordpossibilieties = dict()  # a dictionary that keeps track of what each space can be, is copied each time, only words that are affected by current word placement are changed each time
ratings = dict()
for x in range(size):
    board += "-"
blockers = int(sys.argv[2])


def makeletterfreq():
    thing = dict()
    for a in range(len(frequencies)):
        thing[frequencies[a]] = a
    return thing


frequencies = makeletterfreq()


def makebucket(word, lastinserted):
    bucket = set()
    for a in range(lastinserted + 1, len(word)):
        if word[a] != "-":
            bucket.add((word[:a] + "-" + word[a + 1:], a))
    if len(bucket) == 1:
        return bucket
    for a in bucket:
        bucket = bucket | makebucket(a[0], a[1])
    return bucket


buckets = dict()  # big dictionary of every bucket for words less than length 7
words = set()
with open(sys.argv[3]) as f:
    for line in f:
        line = line.strip()
        if line.isalpha():
            line = line.upper()
            words.add(line)
            if len(line) < 8:
                for a in makebucket(line, -1):
                    a = a[0]
                    if a in buckets:
                        buckets[a].add(line)
                    else:
                        buckets[a] = set()
                        buckets[a].add(line)


def printboard(board):
    if board is None:
        print("fail")
    else:
        for a in range(0, len(board), width):
            print(board[a:a + width:])
    print()


def insert(board, index, character):
    return board[:index] + character + board[index + 1:]


def indextocoord(index):
    return index % width, index // width


def coordtoindex(xy):
    return xy[0] + xy[1] * width


# inserting seed words
# flood fill works
def isconnected(board):
    global width
    if board is None:
        return False
    if board.count("-") == 0:
        return True
    fringe = []
    visited = set()
    start = random.randint(0, len(board) - 1)
    while board[start] != "-":
        start = random.randint(0, len(board) - 1)
    # start = board.find("-")
    fringe.append(start)
    visited.add(start)
    while len(fringe) > 0:
        cur = fringe.pop()
        directions = []
        x, y = indextocoord(cur)
        if x > 0:
            directions.append(-1)
        if x < width - 1:
            directions.append(1)
        if y > 0:
            directions.append(-width)
        if y < height - 1:
            directions.append(width)
        for a in directions:
            if cur + a not in visited:
                if 0 <= cur + a < len(board):
                    if board[cur + a] == "-" or board[cur + a].isalpha():
                        visited.add(cur + a)
                        fringe.append(cur + a)
    if len(visited) == len(board) - board.count("#"):
        return True
    indices = [i for i, x in enumerate(board) if x == "#"]
    indices = set(indices)
    toreturn = allindeces - visited - indices
    if 2 * len(visited) < len(toreturn):
        return visited
    return toreturn


def impliedsquares(board, index,
                   numblocked):  # insert block at index, if goes over block total return None, if cuts off board return None
    # go left right up down and if there is a sequence of less than 3 -'s, call method on all those spaces, numblocked is what spaces blocking hte initial space blocked
    global width
    if board is None or board[index].isalpha() or board[abs(len(board) - index - 1)].isalpha():
        return None, numblocked
    if index == len(board) // 2:
        numblocked.append(index)
        return insert(board, index, "#"), numblocked
    if index in numblocked:
        return board, numblocked
    board = insert(board, index, "#")
    board = insert(board, abs(len(board) - index - 1), "#")
    numblocked.append(index)
    numblocked.append(abs(len(board) - index - 1))
    if len(numblocked) > blockers:
        return None, numblocked
    toblock = []
    u = index - width
    cur = []
    while u >= 0:
        if board[u] != "#":
            cur.append(u)
        else:
            if len(cur) < 3:
                toblock = toblock + cur
            cur = []
        u += -width
    if len(cur) < 3:
        toblock = toblock + cur
    d = index + width
    cur = []
    while d < len(board):
        if board[d] != "#":
            cur.append(d)
        else:
            if len(cur) < 3:
                toblock = toblock + cur
            cur = []
        d += width
    if len(cur) < 3:
        toblock = toblock + cur
    h = index // width
    l = index - 1
    cur = []
    while l >= h * width:
        if board[l] != "#":
            cur.append(l)
        else:
            if len(cur) < 3:
                toblock = toblock + cur
            cur = []
        l += -1
    if len(cur) < 3:
        toblock = toblock + cur
    r = index + 1
    cur = []
    while r < (h + 1) * width:
        if board[r] != "#":
            cur.append(r)
        else:
            if len(cur) < 3:
                toblock = toblock + cur
            cur = []
        r += 1
    if len(cur) < 3:
        toblock = toblock + cur
    if len(numblocked) + 2 * len(
            toblock) > blockers:  # if adding this square now makes it too many blockers, those squares also shouldnt be placed
        return None, numblocked + toblock
    for a in toblock:
        if board is not None:
            if board[a].isalpha():
                return None, numblocked
            if board[a] == "-" and numblocked is not None and a not in numblocked:
                board, numblocked = impliedsquares(board, a, numblocked)
    return board, numblocked


def spaceh(board,
           index):  #
    implied = impliedsquares(board,index,[])
    board = implied[0]
    if len(implied[1])==0:
        print(implied)
    implied = len(implied[1])
    if board is None:
        return 100000000
    blocklengths = []
    u = index - width
    cur = 0
    while u >= 0:
        if board[u] != "#":
            cur += 1
        else:
            break
        u += -width
    blocklengths.append(cur+1)
    d = index + width
    cur = 0
    while d < len(board):
        if board[d] != "#":
            cur += 1
        else:
            break
        d += width
    blocklengths.append(cur+1)
    h = index // width
    l = index - 1
    cur = 0
    while l >= h * width:
        if board[l] != "#":
            cur += 1
        else:
            break
        l += -1
    blocklengths.append(cur+1)
    r = index + 1
    cur = 0
    while r < (h + 1) * width:
        if board[r] != "#":
            cur += 1
        else:
            break
        r += 1
    blocklengths.append(cur+1)
    totalscore = ((blocklengths[0]*blocklengths[1]) + (blocklengths[2]*blocklengths[3]))/implied
    return 100000000-totalscore


def sortindices(board,
                indexs):  # implement heuristic for a space, distance from blocking squares/edges in all 4 directions(space away *2?) + implied squares
    heap = []
    for a in indexs:
        rate = spaceh(board, a)
        heappush(heap, (rate, a))
    return heap


def backtracking(board, numblocked):  # places blocking squares
    if board is None:
        return None
    if numblocked == blockers:
        return board
    if numblocked > blockers:
        return None
    indices = [i for i, x in enumerate(board) if x == "-"]
    indices = sortindices(board, indices)
    while indices:
        a = heappop(indices)
        b, block = impliedsquares(board, a[1], [])
        if b is not None:
            c = backtracking(b, b.count("#"))
            if c is not None:
                return c
    return None


def insertword(board, index, word, direction):
    temp = board
    if direction == "V" or direction == "v":
        for a in word:
            temp = insert(temp, index, a)
            index += width
    else:
        for a in word:
            temp = insert(temp, index, a)
            index += 1
    return temp


def listofwords(board):  # list of tuples of indexes that make words
    visited = set()
    words = []
    for a in range(len(board)):
        if board[a] != "#" and a not in visited:
            visited.add(a)
            coord = indextocoord(a)
            if coord[0] == 0:
                cur = (a,)
                r = a + 1
                while r < (coord[1] + 1) * width:
                    if board[r] == "#":
                        break
                    else:
                        cur += (r,)
                        r += 1
                words.append(cur)
            elif board[a - 1] == "#":
                cur = (a,)
                r = a + 1
                while r < (coord[1] + 1) * width:
                    if board[r] == "#":
                        break
                    else:
                        cur += (r,)
                        r += 1
                words.append(cur)
            if coord[1] == 0:
                cur = (a,)
                d = a + width
                while d < len(board):
                    if board[d] == "#":
                        break
                    else:
                        cur += (d,)
                        d += width
                words.append(cur)
            elif board[a - width] == "#":
                cur = (a,)
                d = a + width
                while d < len(board):
                    if board[d] == "#":
                        break
                    else:
                        cur += (d,)
                        d += width
                words.append(cur)
    return words


def rateword(word):
    score = 0
    for a in word:
        score += frequencies[a]
    return score


for a in words:
    ratings[a] = rateword(a)


def sortpossible(possible):
    sorted = []
    for a in possible:
        heappush(sorted, (ratings[a], a))
    return sorted


for a in buckets:
    buckets[a] = sortpossible(buckets[a])


# returns the possible words that can go in a given space
def getpossiblemoves(word):
    l = len(word)
    if len(word) < 7:
        if word in buckets:
            return buckets[word]
        else:
            return []
    possible = set()
    for a in words:
        if len(a) == l:
            val = True
            for b in range(l):
                if word[b] != a[b] and word[b] != "-":
                    val = False
                    break
            if val is True:
                possible.add(a)
    return sortpossible(possible)


# return the list of indexes that make up the word with the least number of possibilities, and those possibilities
# solved is a set of lists that show which words are solved
def getmostconstrained(possibledict):
    minlen = 99999
    minindex = ()
    minmoves = []
    for a in possibledict:
        b = possibledict[a]
        moves = len(b)
        if 0 < moves < minlen:
            minlen = moves
            minindex = a
            minmoves = b
    return minindex, minmoves


def update(board, indexs, curwords, possibledict, word,used):
    if indexs[1] - indexs[0] == 1:
        direction = "H"
    else:
        direction = "V"
    possible = getpossiblemoves(word)
    possibledict[indexs] = possible
    # if len(possible) == 0:
    #     return None
    if len(possible) == 1:
        word = possible[0]
    curwords[indexs] = word
    edited = []
    for a in indexs:
        if board[a] == "-":
            edited.append(a)
    board = insertword(board, indexs[0], word[1], direction)
    for indv in edited:
        for otherword in wordconnection[indv]:
            if otherword != indexs:
                other = ""
                for index in otherword:
                    other += board[index]
                curwords[otherword] = other
                possible1 = getpossiblemoves(other)
                if len(possible1) == 0:
                    if other not in words:
                        return None
                    if (ratings[other],other) in used:
                        return None
                    used.add(other)
                possibledict[otherword] = possible1
    return board


def goalcheck(possibledict):
    for a in possibledict.values():
        if len(a) != 0:
            return False
    return True
    # if "-" not in possibledict:
    #     return True
    # return False


def solve(board, used, possibledict,
          curwords):  # string of the board, all used words, dict of the possibilities of each word, word currently in each space
    if board is None:
        return None
    if goalcheck(possibledict):
        return board
    used1 = used.copy()
    tempdict = possibledict.copy()
    tempwords = curwords.copy()
    toinsert, moves = getmostconstrained(possibledict)
    for a in moves:
        if a not in used:
            used1.add(a)
            temp = update(board, toinsert, tempwords, tempdict, a,used1)
            if temp is not None:
                result = solve(temp, used1, tempdict, tempwords)
                if result is not None:
                    return result
            used1.remove(a)
    return None


for x in range(4, len(sys.argv)):
    seed = sys.argv[x].split("x")
    dir = seed[0][0]
    heightw = int(seed[0][1:])
    widthw = ""
    word = ""
    for a in seed[1]:
        if a != "#" and not a.isalpha():
            widthw += a
        else:
            word += a
    widthw = int(widthw)
    index = heightw * width + widthw
    board = insertword(board, index, word.upper(), dir)
if blockers == width * height:
    board = ""
    for x in range(size):
        board += "#"
    print(board)
else:
    indices = [i for i, x in enumerate(board) if x == "#"]
    for a in indices:
        board = impliedsquares(board, a, [])[0]
    b = board.count("#")
    if b == blockers:
        None
    else:
        board = backtracking(board, b)
wordlists = listofwords(board)
for a in wordlists:
    for b in a:
        if b in wordconnection:
            wordconnection[b].append(a)
        else:
            wordconnection[b] = [a, ]
for a in wordlists:
    word = ""
    for index in a:
        word += board[index]
    wordpossibilieties[a] = getpossiblemoves(word)
    curword[a] = word
#board = "-------#--------------#--------------#----------#----####-------#----##---------#---#-----------#-----###---#---#---#---###-----#-----------#---#---------##----#-------####----#----------#--------------#--------------#-------"
#board = "##----##-----------#------------#---------#-----#-------#---#---------#----###------#------###----#---------#---#-------#-----#---------#------------#-----------##----##"
printboard(board)
printboard(solve(board, set(), wordpossibilieties, curword))
print(time.perf_counter()-begin)
# print(getpossiblemoves("B-ES"))
#         #solve
