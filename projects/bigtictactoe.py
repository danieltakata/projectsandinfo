import turtle
import random
import math
import time
marks = ('X','O','C')
colors = ('blue','red','black')
def filledMatch(alist, sign=''):
##alist being any possible line of victory (row, column, or
##diagonal), returns True if alist has been won and False otherwise.
##Optional "sign" argument restricts query to the victory of the
##given player.
    if sign != '' and alist[0] != sign:
        return False
    elif alist[0] not in (0,1):
        return False
    for el in alist[1:]:
        if el != alist[0]:
            return False
    return True
class TicTacToe:
    def __init__(self,start=str):
        self.grid = [[start() for i in range(3)] for j in range(3)]
        self.start = start
        self.winner = ''
    def isComplete(self):
##Uses filledMatch on every possible line of victory, sets winner
##if complete, and returns True if complete and False if not.
        for row in self.grid:
            if filledMatch(row):
                self.winner = row[0]
                return True
        for col in range(3):
            if filledMatch([row[col] for row in self.grid]):
                self.winner = self.grid[0][col]
                return True
        if filledMatch([self.grid[diag][2-diag] for diag in range(3)]):
            self.winner = self.grid[2][0]
            return True
        if filledMatch([self.grid[diag][diag] for diag in range(3)]):
            self.winner = self.grid[0][0]
            return True
        for row in self.grid:
            if self.start() in row:
                return False
        self.winner = 2
        return True
    def moveWins(self,row,col,sign):
##Returns True if the given move wins the game for the given 
##sign and False otherwise. Used in computer's move assessment.
        gridCopy = [[cell for cell in row] for row in self.grid]
        gridCopy[row][col] = sign
        for row in gridCopy:
            if filledMatch(row,sign):
                return True
        for col in range(3):
            if filledMatch([row[col] for row in gridCopy],sign):
                return True
        if filledMatch([gridCopy[diag][2-diag] for diag in range(3)],sign):
            return True
        if filledMatch([gridCopy[diag][diag] for diag in range(3)],sign):
            return True
        return False
    def countMarks(self, sign):
##Returns the number of occurences of sign in self.grid. 
##Used in computer's move assessment.
        count = 0
        for i in range(3):
            count += self.grid[i].count(sign)
        return count
    def move(self,row,col,sign):
        if self.start != str:
            raise TypeError
        if self.grid[row][col] != '':
            raise IndexError
        self.grid[row][col] = sign
        if self.isComplete():
            return self.winner
        return -1
    def __eq__(self,right):
        if type(right) != TicTacToe:
            return False
        return self.winner == '' and right.winner == ''
class Board(TicTacToe):
    def __init__(self):
        TicTacToe.__init__(self,TicTacToe)
        self.begin = 0
        self.end = 0
    def isComplete(self):
        for row in range(len(self.grid)):
            if filledMatch(self.grid[row]):
                self.winner = self.grid[row][0]
                self.begin = (3,row+.5)
                self.end = (0,row+.5)
                return True
        for col in range(3):
            if filledMatch([row[col] for row in self.grid]):
                self.winner = self.grid[0][col]
                self.begin = (col+.5,3)
                self.end = (col+.5,0)
                return True
        if filledMatch([self.grid[diag][2-diag] for diag in range(3)]):
            self.winner = self.grid[2][0]
            self.begin = (0,3)
            self.end = (3,0)
            return True
        if filledMatch([self.grid[diag][diag] for diag in range(3)]):
            self.winner = self.grid[0][0]
            self.begin = (0,0)
            self.end = (3,3)
            return True
        for row in self.grid:
            if self.start() in row:
                return False
        self.winner = 2
        return True
    def move(self,row1,col1,row2,col2,sign):
        if not isinstance(self.grid[row1][col1],TicTacToe):
            raise IndexError
        ans = self.grid[row1][col1].move(row2,col2,sign)
        if ans != -1:
            self.grid[row1][col1] = ans
        return ans
class Display:
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.pos = (-1,-1)
        self.tut1 = turtle.Turtle()
        self.tut2 = turtle.Turtle()
        self.tut3 = turtle.Turtle()
        self.screen = self.tut1.getscreen()
        self.screen.setup(845,845,0,0)
        self.screen.setworldcoordinates(-1,-1,4,4)
        self.screen.delay(0)
        self.tut1.ht()
        self.tut2.ht()
        self.tut3.ht()
        for x in (1,2):
            self.tut1.pu()
            self.tut2.pu()
            for y in (0,3):
                self.tut1.goto(x,y)
                self.tut2.goto(y,x)
                self.tut1.pd()
                self.tut2.pd()
        for a in range(3):
            for b in range(3):
                for x in (2,3):
                    self.tut1.pu()
                    self.tut2.pu()
                    for y in (1,4):
                        self.tut1.goto(x/5.0 + a,y/5.0 + b)
                        self.tut2.goto(y/5.0 + a,x/5.0 + b)
                        self.tut1.pd()
                        self.tut2.pd()
        self.tut1.pu()
        self.highlight()
        self.screen.onscreenclick(self.play)
        self.screen.listen()
    def think(self):
        lst = [-float("inf") for _ in range(81)]
        if self.pos == (-1,-1):
            for row1 in range(3):
                for col1 in range(3):
                    if type(self.board.grid[row1][col1]) == TicTacToe:
                        for row2 in range(3):
                            for col2 in range(3):
                                if self.board.grid[row1][col1].grid[row2][col2] == '':
                                    i = col2+row2*3+col1*9+row1*27
                                    lst[i] = 0.0
                                    if type(self.board.grid[row2][col2]) == TicTacToe:
                                        lst[i] += -.5*self.board.grid[row2][col2].countMarks((self.turn+1)%2) - .25*self.board.grid[row2][col2].countMarks(self.turn)
                                    else:
                                        lst[i] -= 2
                                    if self.board.grid[row1][col1].moveWins(row2,col2,self.turn):
                                        lst[i] += 2
                                        if self.board.moveWins(row1,col1,self.turn):
                                            lst[i] += 100
                                    if self.board.moveWins(row2,col2,(self.turn+1)%2):
                                        lst[i] -= 3
        else:
            for row in range(3):
                for col in range(3):
                    if self.board.grid[self.pos[0]][self.pos[1]].grid[row][col] == '':
                        i = col+row*3+self.pos[1]*9+self.pos[0]*27
                        lst[i] = 0.0
                        if type(self.board.grid[row][col]) == TicTacToe:
                            lst[i] += -.5*self.board.grid[row][col].countMarks((self.turn+1)%2) - .25*self.board.grid[row][col].countMarks(self.turn)
                        else:
                            lst[i] -= 2
                        if self.board.grid[self.pos[0]][self.pos[1]].moveWins(row,col,self.turn):
                            lst[i] += 2
                            if self.board.moveWins(self.pos[0],self.pos[1],self.turn):
                                lst[i] += 100
                        if self.board.moveWins(row,col,(self.turn+1)%2):
                            lst[i] -= 3
        indices = []
        highest = lst[0]
        for i in range(81):
            if lst[i] > highest:
                highest = lst[i]
                indices = [i]
            elif lst[i] == highest:
                indices.append(i)
        index = random.choice(indices)
        col2 = index % 3
        index = index // 3
        row2 = index % 3
        index = index // 3
        col1 = index % 3
        index = index // 3
        row1 = index % 3
        x = (col2 + 1.5)/5 + col1
        y = (row2 + 1.5)/5 + row1
        self.play(x,y)
    def highlight(self):
        self.tut3.reset()
        self.tut3.ht()
        self.tut3.pensize(5)
        self.tut3.pencolor(colors[self.turn])
        self.tut3.pu()
        if self.pos == (-1,-1):
            self.tut3.goto(0,0)
            length = 3
        else:
            self.tut3.goto(self.pos[1],self.pos[0])
            length = 1
        self.tut3.pd()
        for i in range(4):
            self.tut3.fd(length)
            self.tut3.lt(90)
        self.tut3.pu()
    def play(self,x,y):
        if self.board.winner != '':
            return
        row1 = math.floor(y)
        col1 = math.floor(x)
        if self.pos == (-1,-1):
            if x < 0 or y < 0 or x > 3 or y > 3:
                return
        elif row1 != self.pos[0] or col1 != self.pos[1]:
            return
        row2 = math.floor((y-row1)*5 - 1)
        col2 = math.floor((x-col1)*5 - 1)
        if row2 not in (0,1,2) or col2 not in (0,1,2):
            return
        try:
            ans = self.board.move(row1,col1,row2,col2,self.turn)
            self.tut1.pencolor(colors[self.turn])
            self.tut1.goto(col1+col2/5+.3,row1+row2/5+.18)
            self.tut1.write(marks[self.turn],False,'center',('comicsans',24,'bold'))
            self.turn = (self.turn+1)%2
            if ans != -1:
                self.tut1.goto(col1+.5,row1-.07)
                self.tut1.pencolor(colors[ans])
                self.tut1.write(marks[ans],False,'center',('comicsans',120,'bold'))
                if self.board.isComplete():
                    self.tut3.reset()
                    self.tut3.ht()
                    if self.board.winner == 2:
                        self.tut1.pencolor(colors[2])
                        self.tut1.goto(1.5,.1)
                        self.tut1.write(marks[2],False,'center',('comicsans',300,"bold"))
                    else:
                        self.tut3.pu()
                        self.tut3.pensize(5)
                        self.tut3.pencolor(colors[self.board.winner])
                        self.tut3.goto(self.board.begin[0],self.board.begin[1])
                        self.tut3.pd()
                        self.tut3.goto(self.board.end[0],self.board.end[1])
                        self.tut3.pu()
                    return
            if type(self.board.grid[row2][col2]) == TicTacToe:
                self.pos = (row2,col2)
            else:
                self.pos = (-1,-1)
        except IndexError:
            return
        self.highlight()
        if self.turn == 1:
            time.sleep(1)
            self.think()
d = Display()
turtle.mainloop()
