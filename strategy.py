import sys
from random import choice

token = ["@", "o"]
myturn = 0
movedir = [-10, 10, -1, 1]
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
corners = [11, 18, 81, 88]
oneoffcorner = [12, 21, 22, 17,27, 28, 82,72, 71, 87, 78,77]
oppdirections = directions[::-1]
board = "??????????" \
        "?........?" \
        "?........?" \
        "?........?" \
        "?...o@...?" \
        "?...@o...?" \
        "?........?" \
        "?........?" \
        "?........?" \
        "??????????"


def possibleMoves(board, turn):
    possible = set()
    global token
    for num, cur in enumerate(board):
        if board[num] == token[-1 * (turn - 1)]:
            for offset in range(len(directions)):
                num1 = num + directions[offset]
                if board[num1] == ".":
                    num2 = num + oppdirections[offset]
                    while board[num2] not in "?.":
                        if board[num2] == token[turn]:
                            possible.add(num1)
                            break
                        num2 = num2 + oppdirections[offset]
    return sorted(list(possible))


def insert(board, turn, index):
    return board[:index] + token[turn] + board[index + 1:]


def move(board, turn, index):
    insert(board, turn, index)
    for offset in range(len(directions)):
        num = index
        num += directions[offset]
        while board[num] not in "?.":
            if board[num] == token[turn]:
                for a in range(index, num, directions[offset]):
                    board = board[:a] + token[turn] + board[a + 1:]
                break
            num += directions[offset]
    return board


def tokensindirection(board, index, direction):
    temp = set()
    index += direction
    while board[index] != "?":
        temp.add(index)
        index += direction
    return temp


def nextto(index):
    temp = []
    for a in movedir:
        if board[index + a] != "?":
            temp.append(index + a)
    return temp


def mobility(board, turn):  # a guess on the mobility of black and white, greater numbers are better for you
    temp = []
    x = possibleMoves(board, turn)
    for a in x:
        temp.append(len(possibleMoves(insert(board, turn, a), (-1 * (turn - 1))), ))
    if len(temp) == 0:
        return -1
    b = min(temp)
    return len(x) - b


def isstable(board, b, mystablepieces):
    if b in mystablepieces:
        return True
    up = tokensindirection(board, b, -10)
    up = len(up) == 0 or (up.issubset(mystablepieces))
    down = False
    if up is False:
        down = tokensindirection(board, b, 10)
        down = len(down) == 0 or (down in mystablepieces)
    if (up or down) is True:
        left = tokensindirection(board, b, -1)
        left = len(left) == 0 or (left in mystablepieces)
        right = False
        if left is False:
            right = tokensindirection(board, b, 1)
            right = len(right) == 0 or (right in mystablepieces)
        if (left or right) is True:
            upr = tokensindirection(board, b, -9)
            upr = len(upr) == 0 or (upr in mystablepieces)
            downl = False
            if upr is False:
                downl = tokensindirection(board, b, 9)
                downl = len(downl) == 0 or (downl in mystablepieces)
            if (upr or downl) is True:
                upl = tokensindirection(board, b, -11)
                upl = len(upl) == 0 or (upl in mystablepieces)
                downr = False
                if upl is False:
                    downr = tokensindirection(board, b, 11)
                    downr = len(downr) == 0 or (downr in mystablepieces)
                if (upl or downr) is True:
                    return True
    return False


def bigheuristic(board, turn, stable):
    mycoins = board.count(token[turn])
    # theircoins = board.count(token[-1 * (turn - 1)])
    # parity = 100 * ((mycoins - theircoins) / (mycoins + theircoins))
    temp = []
    tempmoves = []
    mymob = possibleMoves(board, turn)
    mymobility = len(mymob)
    # if mymobility > 0:
    #     for a in mymob:
    #         tempmoves.append(possibleMoves(move(board, turn, a), (-1 * (turn - 1))))
    #         temp.append(len(tempmoves[len(tempmoves) - 1]))
    #     theirmobility = min(temp)
    #     ourpotentialmobility = 100 * ((mymobility - theirmobility) / (mymobility + theirmobility))
    # else:
    #     ourpotentialmobility = -100
    mycorner = 0
    # theircorner = 0
    # if stable == True:
    #     mystablepieces = set()
    #     for a in corners:
    #         if board[a] == token[turn]:
    #             mystablepieces.add(a)
    #             if a == 11:
    #                 if board[12] == token[turn]:
    #                     mystablepieces.add(12)
    #                     b = 13
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += 1
    #                 if board[21] == token[turn]:
    #                     mystablepieces.add(21)
    #                     b = 31
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += 10
    #                 if board[22] == token[turn]:
    #                     mystablepieces.add(22)
    #                     b = 33
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += 11
    #             if a == 18:
    #                 if board[17] == token[turn]:
    #                     mystablepieces.add(17)
    #                     b = 16
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += -1
    #                 if board[28] == token[turn]:
    #                     mystablepieces.add(28)
    #                     b = 38
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += 10
    #                 if board[27] == token[turn]:
    #                     mystablepieces.add(27)
    #                     b = 36
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += 9
    #             if a == 81:
    #                 if board[82] == token[turn]:
    #                     mystablepieces.add(82)
    #                     b = 83
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += 1
    #                 if board[71] == token[turn]:
    #                     mystablepieces.add(71)
    #                     b = 61
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += -10
    #                 if board[72] == token[turn]:
    #                     mystablepieces.add(72)
    #                     b = 63
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += -9
    #             if a == 88:
    #                 if board[87] == token[turn]:
    #                     mystablepieces.add(87)
    #                     b = 86
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += -1
    #                 if board[78] == token[turn]:
    #                     mystablepieces.add(78)
    #                     b = 68
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += -10
    #                 if board[77] == token[turn]:
    #                     mystablepieces.add(77)
    #                     b = 66
    #                     while board[b] == token[turn]:
    #                         mystablepieces.add(b)
    #                         b += -11
    #     for a in corners:
    #         if board[a]==token[turn]:
    #             for b in nextto(a):
    #                 if board[b]==token[turn]:
    #                         if isstable(board,b,mystablepieces):
    #                             for c in nextto(b):
    #                                 if board[c]==token[turn]:
    #                                     if isstable(board,c,mystablepieces):
    #                                         mystablepieces.add(c)
    #                                         for d in nextto(c):
    #                                             if board[d]==token[turn]:
    #                                                 if isstable(board,d,mystablepieces):
    #                                                     mystablepieces.add(d)
    for a in corners:
        if board[a] == token[turn]:
            mycorner += 1
        # if board[a] != ".":
        #      theircorner += 1
    # for b in mymob:
    #     if b in corners:
    #         mycorner += 1
    # for c in possibleMoves(board, (-1 * (turn - 1))):
    #     if c in corners:
    #         theircorner += 1
    # if mycorner + theircorner > 0:
    #     corner = 100 * ((mycorner - theircorner) / (mycorner + theircorner))
    # else:
    #     corner = 0
        # return 10 * parity + 10 * len(mystablepieces)+4*ourpotentialmobility
    return mycoins*.5+ mymobility + mycorner*500


def position(board, turn, matrixx):
    sum = 0
    for a in possibleMoves(board, turn):
        sum += matrixx[a]
    return sum


def minimax(board, turn, alpha, beta, depth, maxd, havecorner):
    if depth == 60:#CHANGES, if the game is order return your number of tokens, ensure the most tokens taken to end the game
        black = board.count("@")
        white = board.count("o")
        if turn == 0:
            return black
        else:
            return white
    if depth == maxd:
        return bigheuristic(board, turn, havecorner)
    else:
        temp = []
        for a in possibleMoves(board, turn):
            temp.append(move(board, turn, a))
        if len(temp) == 0:
            return -1
        if turn == 0:
            tempn = []
            for b in temp:
                c = minimax(b, 1, alpha, beta, depth + 1, maxd, havecorner)
                tempn.append(c)
                if c > alpha:#PRUNING
                    alpha = c
                if alpha >= beta:
                    break
            return max(tempn)
        else:
            tempn = []
            for b in temp:
                c = minimax(b, 0, alpha, beta, depth + 1, maxd, havecorner)
                tempn.append(c)
                if c < beta:
                    beta = c
                if alpha >= beta:#PRUNING
                    break
            return min(tempn)


class Strategy():
    def best_strategy(self, board, player, best_move, still_running):
        blank = board.count(".")
        depth = 60 - blank
        if player == "@":
            myturn = 0
        else:
            myturn = 1
        onemoveaway = []
        possible = possibleMoves(board, myturn)
        for a in possibleMoves(board, myturn):
            if a in corners:
                best_move.value = a
                while 1 == 1:
                    None
            onemoveaway.append((a, move(board, myturn, a)))
        if len(onemoveaway) == 0:
            return -1
        stable = False
        for a in corners:
            if board[a] == player:
                for b in nextto(a):
                    if b in possible:
                        best_move.value = b
                        while 1 == 1:
                            None
                stable = True
        for x in range(1,61):
            # print(best_move.value)
            omascores = []
            alpha = -1000000000000000000000
            for b in onemoveaway:
                d = minimax(b[1], -1 * (myturn - 1), alpha, 100000000000000000, depth, x + depth, stable)
                if d > alpha:
                    alpha = d
                omascores.append((d, b[0]))
            if myturn == 0:
                b = max(omascores)
                best_move.value = b[1]
                while best_move.value in oneoffcorner and len(omascores) > 1:
                    omascores.remove(b)
                    b = max(omascores)
                    best_move.value = b[1]
            else:
                b = min(omascores)
                best_move.value = b[1]
                while best_move.value in oneoffcorner and len(omascores) > 1:
                    omascores.remove(b)
                    b = min(omascores)
                    best_move.value = b[1]


def idminimax(board, player):
    best_move = -1
    blank = board.count(".")
    depth = 60 - blank
    if player == "@":
        myturn = 0
    else:
        myturn = 1
    onemoveaway = []
    possible = possibleMoves(board, myturn)
    for a in possibleMoves(board, myturn):
        if a in corners:
            print(a)
            while 1 == 1:
                None
        onemoveaway.append((a, move(board, myturn, a)))
    if len(onemoveaway) == 0:
        return -1
    stable = False
    for a in corners:
        if board[a] == player:
            for b in nextto(a):
                if b in possible:
                    print(b)
                    while 1 == 1:
                        None
            stable = True
    for x in range(1,4):
        # print(best_move)
        omascores = []
        alpha = -1000000000000000000000
        for b in onemoveaway:
            d = minimax(b[1], -1 * (myturn - 1), alpha, 100000000000000000, depth, x + depth, stable)
            if d > alpha:
                alpha = d
            omascores.append((d, b[0]))
        if myturn == 0:
            b = max(omascores)
            best_move = b[1]
            while best_move in oneoffcorner and len(omascores) > 1:
                omascores.remove(b)
                b = max(omascores)
                best_move = b[1]
        else:
            b = min(omascores)
            best_move = b[1]
            while best_move in oneoffcorner and len(omascores) > 1:
                omascores.remove(b)
                b = min(omascores)
                best_move = b[1]
        print(best_move)


def printboard(board):
    for a in range(0, len(board), 10):
        print(board[a:a + 10:])


# idminimax(sys.argv[1], sys.argv[2])