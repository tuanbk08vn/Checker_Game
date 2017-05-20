import copy
import random
import math
# ======================== Class Player =======================================
class Player:
    def __init__(self, str_name):
        self.str = str_name
        self.currPlayer = str_name
        self.oppoPlayer = ""

    def __str__(self):
        return self.str

    k = 0  # level of tree every times ( = times of recursion)
    isKing = False
    minor = 0  # == 1 is meant to have second position to go already
    listResult = []  # declare list for every round
    copyListResult = [] #a copy of list Result
    jumpNumber = []
    visited = [[0] * 8 for _ in range(8)]  # assign value 0 to unvisited piece for all board
    treeLevel = 0  #level which we are searching in
    maxTreeLevel = 3 #maximum level which we want to search as depth first
    #get last index in list
    def last_index(self):
        return len(self.listResult) - 1
    #get last element in last index
    def last_element(self):
        if len(self.listResult) > 0:
            outLength = len(self.listResult) - 1
        else:
            outLength = 0
        if not self.listResult:
            return 1
        else:
            inLength = len(self.listResult[outLength]) - 1
        # if inLength < 1 or len(self.listResult[outLength]) < 1:
        #     return 1
            return inLength


    #listMove method provide list of moves at every round
    def listMove(self, currPlayer, state=[[]*8]*8):
        self.currPlayer = currPlayer
        if currPlayer == 'r':
            self.oppoPlayer = 'b'
        elif currPlayer == 'b':
            self.oppoPlayer = 'r'
        self.listResult = []
        if currPlayer == 'b':
            for i in [7,6,5,4,3,2,1,0]:
                for j in range(0,8):
                    self.visited = [[0] * 8 for _ in range(8)]
                    self.k = 0
                    if state[i][j] == 'R' or state[i][j] == 'B':
                        self.isKing = True
                    else:
                        self.isKing = False
                    self.pieceMove(i,j, state) #invoke recursive this method for each man
        else:
            for i in [0,1,2,3,4,5,6,7]:
                for j in range(0, 8):
                    self.visited = [[0] * 8 for _ in range(8)]
                    self.k = 0
                    if state[i][j] == 'R' or state[i][j] == 'B':
                        self.isKing = True
                    else:
                        self.isKing = False
                    self.pieceMove(i, j, state)  # invoke recursive this method for each man
        if len(self.jumpNumber) < 1 and len(self.listResult) > 0:
            return self.listResult
        elif len(self.jumpNumber) > 0 and len(self.listResult) > 0:
            listResult_1 = []
            listResult_1.append(self.listResult[self.jumpNumber[0]])
            self.jumpNumber.clear()
            return listResult_1
           # listResult_1 = self.listResult[self.jumpNumber]
            # if len()>0 and len(self.listResult)>0:
            #     for k in range(0,len()):
            #     for k in range(0, len()):
        # self.listResult = []
        #         listResult_1.append(self.listResult[[0]])

            # listResult_1.append(self.listResult[0])
            # return self.listResult[0]
            #return []
        #return self.listResult
        else:
            return []
    #add valuable options into listResult
    def pieceMove(self,i, j,state=[[]*8]*8):
        self.k += 1
        if state[i][j] == self.currPlayer or state[i][j].lower()==self.currPlayer or self.minor == 1:
            #first direction
            if (i+1)<=7 and (j+1)<=7 and (self.currPlayer != 'r' or self.isKing == True):
                #option diagonal
                if state[i + 1][j + 1] == '.' and (self.visited[i][j] == 0 or self.k == 1):
                    #set List 'visited' = 0 for all board
                    for m in range(0,8):
                        for n in range(0,8):
                            self.visited[m][n] = 0
                    self.listResult.append([(i,j),(i+1,j+1)]) #append diagonal

                    self.visited[i][j] = 1
                    self.visited[i+1][j+1] = 1
                #option jump to eat opponent
                elif (i+2)<=7 and (j+2)<= 7:
                    if state[i+1][j+1] == self.oppoPlayer and state[i+2][j+2] == '.' and self.visited[i+2][j+2] != 1: #if diagonal cell is opponent and the next diagonal cell is '.'
                        #jump from second time
                        if self.minor == 1:
                            insert_index = self.last_index()
                            if self.visited[i+2][j+2] != 1:
                                self.listResult[insert_index].append((i + 2, j + 2))
                                self.visited[i+2][j+2] = 1
                        #jump at first time
                        else:
                            #listResult is empty
                            if not self.listResult:
                                #index = 1
                                self.minor = 1
                                #insert_index = self.last_index()
                                self.listResult.append([(i, j)])
                                self.listResult[0].append((i + 2, j + 2))
                                self.visited[i][j] = 1
                                self.visited[i + 2][j + 2] = 1
                            #listResult is not empty
                            else:
                                index = self.last_element()
                            #copy previous sub list
                            if self.visited[i][j] == 1 or (self.listResult[len(self.listResult)-1][index-1][0] == i and self.listResult[len(self.listResult)-1][index-1][1] == j) :
                                copy_index = self.last_index()
                                copy_last = copy.deepcopy(self.listResult[copy_index])
                                for t in range(len(copy_last)-self.k+1):
                                    del copy_last[len(copy_last)-1]
                                    #del copy_last[len(copy_last) - 1]
                                #copy = copy.pop(len(copy_last)-2)
                                self.listResult.append(copy_last)

                                self.minor = 1
                                insert_index = self.last_index()
                                self.listResult[insert_index].append((i, j))
                                self.listResult[insert_index].append((i + 2, j + 2))
                                self.visited[i][j] = 1
                                self.visited[i + 2][j + 2] = 1
                                if len(self.jumpNumber) == 0:
                                    self.jumpNumber.append(len(self.listResult) - 1)
                            #add first position into listResult (man's include original position)
                            else:
                                self.listResult.append([(i, j),(i+2,j+2)])
                                self.visited[i][j] = 1
                                self.visited[i+2][j+2] = 1
                                self.minor = 1
                                if len(self.jumpNumber) == 0:
                                    self.jumpNumber.append(len(self.listResult) - 1)
                        self.pieceMove(i+2,j+2,state)
                    self.visited[i + 2][j + 2] = 0
            #====================================================================================
            #second direction
            if (i+1)<=7 and (j-1)>=0 and (self.currPlayer != 'r' or self.isKing == True):
                if state[i+1][j-1] == '.' and (self.visited[i][j] == 0 or self.k == 1):  #if diagonal cell is empty
                    for m in range(0,8):
                        for n in range(0,8):
                            self.visited[m][n] = 0
                    self.listResult.append([(i, j),(i+1,j-1)])
                    self.visited[i][j] = 1
                    self.visited[i+1][j-1] = 1
                elif (i+2)<=7 and (j-2)>= 0:
                    if state[i+1][j-1] == self.oppoPlayer and state[i+2][j-2]=='.' and self.visited[i+2][j-2] != 1: #if diagonal cell is opponent and the next diagonal cell is '.'
                        if self.minor == 1:
                            insert_index = self.last_index()
                            if self.visited[i + 2][j - 2] != 1:
                                self.listResult[insert_index].append((i + 2, j - 2))
                                self.visited[i+2][j-2] = 1
                        else:
                            if not self.listResult:
                                self.minor = 1
                                self.listResult.append([(i, j)])
                                self.listResult[0].append((i + 2, j - 2))
                                self.visited[i][j] = 1
                                self.visited[i + 2][j - 2] = 1
                            else:
                                index = self.last_element()
                            if self.visited[i][j] == 1 or (self.listResult[len(self.listResult) - 1][index-1][0] == i and self.listResult[len(self.listResult) - 1][index-1][1] == j):
                                copy_index = self.last_index()
                                copy_last = copy.deepcopy(self.listResult[copy_index])
                                for t in range(len(copy_last)-self.k+1):
                                    del copy_last[len(copy_last)-1]
                                self.listResult.append(copy_last)

                                self.minor = 1
                                insert_index = self.last_index()
                                self.listResult[insert_index].append((i, j))
                                self.listResult[insert_index].append((i + 2, j - 2))
                                self.visited[i][j] = 1
                                self.visited[i + 2][j - 2] = 1
                                if len(self.jumpNumber) == 0:
                                    self.jumpNumber.append(len(self.listResult) - 1)
                            else:
                                self.minor = 1
                                self.listResult.append([(i, j),(i+2,j-2)])
                                self.visited[i][j] = 1
                                self.visited[i+2][j-2] = 1
                                if len(self.jumpNumber) == 0:
                                    self.jumpNumber.append(len(self.listResult) - 1)
                        self.pieceMove(i+2,j-2,state)
                    self.visited[i + 2][j - 2] = 0
            # ====================================================================================
            #third direction
            if (i-1)>=0 and (j-1)>=0 and (self.currPlayer != 'b' or self.isKing == True):
                if state[i-1][j-1] == '.' and (self.visited[i][j] == 0 or self.k == 1):  #if diagonal cell is empty
                    for m in range(0,8):
                        for n in range(0,8):
                            self.visited[m][n] = 0
                    self.listResult.append([(i, j),(i-1,j-1)])
                    self.visited[i][j] = 1
                    self.visited[i-1][j-1] = 1
                elif (i-2)>=0 and (j-2)>= 0:
                    if state[i-1][j-1] == self.oppoPlayer and state[i-2][j-2]=='.' and self.visited[i-2][j-2] != 1: #if diagonal cell is opponent and the next diagonal cell is '.'
                        if self.minor == 1:
                            insert_index = self.last_index()
                            if self.visited[i - 2][j - 2] != 1:
                                self.listResult[insert_index].append((i - 2, j - 2))
                                self.visited[i-2][j-2] = 1
                        else:
                            if not self.listResult:
                                self.minor = 1
                                self.listResult.append([(i, j)])
                                self.listResult[0].append((i - 2, j - 2))
                                self.visited[i][j] = 1
                                self.visited[i - 2][j - 2] = 1
                            else:
                                index = self.last_element()
                            if self.visited[i][j] == 1 or (self.listResult[len(self.listResult) - 1][index-1][0] == i and self.listResult[len(self.listResult) - 1][index-1][1] == j):
                                copy_index = self.last_index()
                                copy_last = copy.deepcopy(self.listResult[copy_index])
                                for t in range(len(copy_last)-self.k+1):
                                    del copy_last[len(copy_last)-1]
                                self.listResult.append(copy_last)

                                self.minor = 1
                                insert_index = self.last_index()
                                self.listResult[insert_index].append((i, j))
                                self.listResult[insert_index].append((i - 2, j - 2))
                                self.visited[i][j] = 1
                                self.visited[i - 2][j - 2] = 1
                                if len(self.jumpNumber) == 0:
                                    self.jumpNumber.append(len(self.listResult) - 1)
                            else:
                                self.minor = 1
                                self.listResult.append([(i, j),(i-2,j-2)])
                                self.visited[i][j] = 1
                                self.visited[i-2][j-2] = 1
                                if len(self.jumpNumber) == 0:
                                    self.jumpNumber.append(len(self.listResult) - 1)
                        self.pieceMove(i-2,j-2,state)
                    self.visited[i - 2][j - 2] = 0
            # ====================================================================================
            #fourth direction
            if (i-1)>=0 and (j+1)<=7 and (self.currPlayer != 'b' or self.isKing == True):
                if state[i-1][j+1] == '.'  and (self.visited[i][j] == 0 or self.k == 1):
                    for m in range(0,8):
                        for n in range(0,8):
                            self.visited[m][n] = 0
                    self.listResult.append([(i, j),(i-1,j+1)])
                    self.visited[i][j] = 1
                    self.visited[i-1][j+1] = 1
                elif (i-2)>=0 and (j+2)<= 7:
                    if state[i-1][j+1] == self.oppoPlayer and state[i-2][j+2]=='.' and self.visited[i-2][j+2] != 1:
                        if self.minor == 1:
                            insert_index = self.last_index()
                            if self.visited[i - 2][j + 2] != 1:
                                self.listResult[insert_index].append((i - 2, j + 2))
                                self.visited[i-2][j+2] = 1
                        else:
                            if not self.listResult:
                                self.minor = 1
                                self.listResult.append([(i, j)])
                                self.listResult[0].append((i - 2, j + 2))
                                self.visited[i][j] = 1
                                self.visited[i - 2][j + 2] = 1

                            else:
                                index = self.last_element()
                            if self.visited[i][j] == 1 or (self.listResult[len(self.listResult) - 1][index - 1][0] == i and self.listResult[len(self.listResult) - 1][index - 1][1] == j):
                                copy_index = self.last_index()
                                copy_last = copy.deepcopy(self.listResult[copy_index])
                                for t in range(len(copy_last)-self.k+1):
                                    del copy_last[len(copy_last)-1]
                                self.listResult.append(copy_last)

                                self.minor = 1
                                insert_index = self.last_index()
                                self.listResult[insert_index].append((i, j))
                                self.listResult[insert_index].append((i - 2, j + 2))
                                self.visited[i][j] = 1
                                self.visited[i - 2][j + 2] = 1
                                if len(self.jumpNumber) == 0:
                                    self.jumpNumber.append(len(self.listResult) - 1)
                            else:
                                self.minor = 1
                                self.listResult.append([(i, j),(i-2,j+2)])
                                self.visited[i][j] = 1
                                self.visited[i-2][j+2] = 1
                                if len(self.jumpNumber) == 0:
                                    self.jumpNumber.append(len(self.listResult) - 1)
                        self.pieceMove(i-2,j+2,state)
                    self.visited[i - 2][j + 2] = 0
            self.minor = 0
        self.k -= 1

# Student MUST implement this function
# The return value should be a move that is denoted by a list of tuples
    def nextMove(self, state):
        #result = self.listMove(self.currPlayer,state)
        #print(result)
        #alpha = self.assessment(state,self.currPlayer)
        #new_state = self.BoardCopy1(state)
        #bestValue = self.alphaBeta(self.listResult,alpha,alpha,True,new_state)
        # children = len(self.listResult)
        # choosenIndex = 0
        # for i in range(0,children):
        #     currentValue = self.assessment(state,self.currPlayer)
        #     if bestValue == currentValue:
        #         break
            #choosenIndex += 1
        result_1 = self.alpha_beta(state, 5, -10000, 10000, True)
        #print(result_1)
        #if len(result_1) != 0:
            # if len(result) > choosenIndex - 1:
        if len(result_1) > 0:
            return result_1[1]
        else:
            return []
        #else:
            #return []

    #assessment function => assess current state
    def assessment(self,state,currentPlayer):
        if currentPlayer == 'r':
            opponentPlayer = 'b'
        elif currentPlayer == 'b':
            opponentPlayer = 'r'
        result = 0
        for i in range(0,8):
            for j in range(0,8):
                if state[i][j] == currentPlayer:
                    result += 1
                elif state[i][j] == currentPlayer.upper():
                    result += 5
                elif state[i][j] == opponentPlayer:
                    result -= 1
                elif state[i][j] ==opponentPlayer.upper():
                    result -= 5
        return result

        # Board Copy
    def BoardCopy1(self,board):
        new_board = [[]] * 8
        for i in range(8):
            new_board[i] = [] + board[i]
        return new_board

    # Change state of board for calculating assessment
    def doit1(self, move, state=[[]*8]*8):
        # new_state = [[]*8]*8
        new_state = self.BoardCopy1(state)
        # Move one step
        # example: [(2,2),(3,3)] or [(2,2),(3,1)]
        if len(move) == 2 and abs(move[1][0] - move[0][0]) == 1:
            new_state[move[0][0]][move[0][1]] = '.'
            if state[move[0][0]][move[0][1]] == 'b' and move[1][0] == 7:
                new_state[move[1][0]][move[1][1]] = 'B'
            elif state[move[0][0]][move[0][1]] == 'r' and move[1][0] == 0:
                new_state[move[1][0]][move[1][1]] = 'R'
            else:
                new_state[move[1][0]][move[1][1]] = state[move[0][0]][move[0][1]]
        # Jump
        # example: [(1,1),(3,3),(5,5)] or [(1,1),(3,3),(5,1)]
        else:
            step = 0
            new_state[move[0][0]][move[0][1]] = '.'
            while step < len(move) - 1:
                new_state[int(math.floor((move[step][0] + move[step + 1][0]) / 2))][
                    int(math.floor((move[step][1] + move[step + 1][1]) / 2))] = '.'
                step = step + 1
            if state[move[0][0]][move[0][1]] == 'b' and move[step][0] == 7:
                new_state[move[step][0]][move[step][1]] = 'B'
            elif state[move[0][0]][move[0][1]] == 'r' and move[step][0] == 0:
                new_state[move[step][0]][move[step][1]] = 'R'
            else:
                new_state[move[step][0]][move[step][1]] = state[move[0][0]][move[0][1]]
        return new_state

    #terminal Node or not -> return True False
    def nodeLeft(self, maxPlayer,state):
        if not maxPlayer:
            opponentPlayer = Player(self.oppoPlayer)
            moves = opponentPlayer.listMove(self.oppoPlayer, state)
            if moves != []:
                return False
            else:
                return True
        else:
            moves = self.listMove(self.currPlayer, state)
            if moves != []:
                return False
            else:
                return True


    #alpha-beta algorithm
    # def alphaBeta1(self,copyListResult, alpha, beta, maximisingPlayer, currentState=[[]*8]*8):
    #     self.treeLevel += 1
    #     bestValue = 0
    #     if self.treeLevel == self.maxTreeLevel:
    #         # if maximisingPlayer:
    #         #     self.copyListResult = self.listMove(self.currentPlayer,currentState)
    #         # else:
    #         #     self.copyListResult = self.listMove(self.oppoPlayer,currentState)
    #         #copyBoard = self.BoardCopy1(currentState)
    #         # state = self.doit1(copyListResult[0],currentState)
    #         bestValue = self.assessment(currentState,self.currPlayer)
    #     elif maximisingPlayer:
    #         bestValue = alpha
    #
    #     #Recurse for all children of node.
    #         copyListResult = self.listMove(self.currPlayer, currentState)
    #         c = len(copyListResult)
    #         gen = (x for x in (0,c) if x < c)
    #
    #         for i in gen:
    #         #while i<c:
    #             tempState = self.doit1(copyListResult[i],currentState)
    #             childValue = self.alphaBeta1(copyListResult[i], bestValue, beta, False,tempState)
    #             bestValue = max(bestValue, childValue)
    #             if beta <= bestValue:
    #                 break
    #             i += 1
    #         self.treeLevel -= 1
    #     else:
    #         bestValue = beta
    #
    #     # Recurse
    #     #for all children of node.
    #     #for vawr i=0, c=node.children.length; i < c; i++:
    #         copyListResult = self.listMove(self.oppoPlayer, currentState)
    #         c = len(copyListResult)
    #         gen = (x for x in (0, c) if x < c)
    #         for i in gen:
    #             tempState = self.doit1(copyListResult[i], currentState)
    #             childValue = self.alphaBeta1(copyListResult[i], alpha, bestValue, True, tempState)
    #             bestValue = min(bestValue, childValue)
    #             if bestValue <= alpha:
    #                 break
    #     return bestValue

    def myMinimax(self, state, level, alpha, beta, maxPlayer):
        if self.nodeLeft(maxPlayer,state) == True or level == 0:
            return [self.assessment(state,self.currPlayer), []]
        if maxPlayer:
            moves = self.listMove(self.currPlayer,state)
        else:
            opponentPlayer = Player(self.oppoPlayer)
            moves = opponentPlayer.listMove(opponentPlayer.currPlayer,state)
        best = moves[0]
        if maxPlayer:
            val = -200
            for move in moves:
                previousVal = val
                val = max(val, self.myMinimax(self.doit1(move, state), level - 1, alpha, beta, False)[0])
                alpha = max(alpha, val)
                if previousVal != val:
                    best = move
                if beta <= alpha:
                    break
            return [val, best]
        else:
            val = -200
            for move in moves:
                previousVal = val
                val = min(val, self.myMinimax(self.doit1(move, state), level - 1, alpha, beta, True)[0])
                beta = min(beta, val)
                if previousVal != val:
                    best = move
                if beta <= alpha:
                    break
            return [val, best]