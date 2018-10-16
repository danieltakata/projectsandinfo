import random
import time
values1 = [i for i in range(2,15)]
values2 = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
values = dict()
for i in range(len(values1)):
    values[values1[i]] = values2[i]
    values[values2[i]] = values1[i]
class Player(object):
    def __init__(self, name=''):
        self.name = name
        self.hand = [[],[],[],[],[]]
    def getName(self):
        return self.name
    def getCards(self):
        return self.hand[0] + self.hand[1] + self.hand[2] + self.hand[3] + self.hand[4]
    def addCard(self, newCard):
        if newCard[0] == '2':
            self.hand[0].append(newCard)
            return
        newSet = [newCard]
        for i in range(3,0,-1):
            for k in range(len(self.hand[i]) - 1,-1,-1):
                if self.hand[i][k][0] == newCard[0]:
                    newSet.append(self.hand[i].pop(k))
        gogo = True
        i = 0
        j = len(newSet)
        while gogo and i < len(self.hand[j]):
            if values[self.hand[j][i][0]] > values[newCard[0]]:
                for k in range(j):
                    self.hand[j].insert(i,newSet.pop())
                gogo = False
            i += 1
        self.hand[j].extend(newSet)
    def addCards(self, newCards):
        for card in newCards:
            self.addCard(card)
    def removeCard(self, oldCard):
        for index in range(5):
            if oldCard in self.hand[index]:
                self.hand[index].remove(oldCard)
                rest = []
                for card in self.hand[index]:
                    if card[0] == oldCard[0]:
                        self.hand[index].remove(card)
                        rest.append(card)
                self.addCards(rest)
                return True
        return False
    def removeCards(self, oldCards):
        result = True
        for card in oldCards:
            result *= self.removeCard(card)
        return result
    def giveBest(self):
        if len(self.hand[0]) > 0:
            return self.hand[0].pop()
        index = 0
        for subhand in range(1,5):
            if len(self.hand[subhand]) > 0:
                if index == 0:
                    index = subhand
                elif values[self.hand[subhand][-1][0]] > values[self.hand[index][-1][0]]:
                    index = subhand
        result = self.hand[index].pop()
        for i in range(index - 1):
            self.hand[index - 1].append(self.hand[index].pop())
        return result
    def giveWorst(self):
        index = 1
        while index <= 4:
            if len(self.hand[index]) > 0:
                for i in range(index - 1):
                    self.hand[index - 1].append(self.hand[index].pop(0))
                return self.hand[index].pop(0)
            else:
                index += 1
    def give2Best(self):
        best = []
        if len(self.hand[0]) > 1:
            best.append(self.hand[0].pop())
            best.append(self.hand[0].pop())
        elif len(self.hand[0]) == 1:
            best.append(self.hand[0].pop())
            index = 0
            for subhand in range(1,5):
                if len(self.hand[subhand]) > 0:
                    if index == 0:
                        index = subhand
                    elif values[self.hand[subhand][-1][0]] > values[self.hand[index][-1][0]]:
                        index = subhand
            best.append(self.hand[index].pop())
            for i in range(index - 1):
                self.hand[index - 1].append(self.hand[index].pop())
        else:
            index = 1
            for subhand in range(2,5):
                if len(self.hand[subhand]) > 0:
                    if index == 1:
                        index = subhand
                    elif values[self.hand[subhand][-1][0]] > values[self.hand[index][-1][0]]:
                        index = subhand
            best.append(self.hand[index].pop())
            best.append(self.hand[index].pop())
            if index > 2:
                rest = []
                for i in range(index - 2):
                    rest.append(self.hand[index].pop())
                for i in range(0,len(self.hand[index - 2])):
                    if values[self.hand[index - 2][i][0]] > values[rest[0][0]]:
                        for card in rest:
                            self.hand[index - 2].insert(i,card)
                        break
        return best
    def give2Worst(self):
        return [self.giveWorst(), self.giveWorst()]
    def play(self, field):
        time.sleep(2)
        power = 0
        move = []
        if len(field) > 0:
            power = values[field[0][0]]
        if len(self.hand[0]) > 0 and len(self.hand[1]) + len(self.hand[2])/2 + \
                                     len(self.hand[3])/3 + len(self.hand[4])/4 == 1:
            move = self.hand[0]
            self.hand[0] = []
            return move
        lowest = len(field)
        if lowest == 0:
            lowest = 1
        for search in range(lowest,6):
            for card in range(0,len(self.hand[search%5]),search):
                if values[self.hand[search%5][card][0]] >= power:
                    if search == 5:
                        move.append(self.hand[0].pop())
                    for i in range(search%5):
                        move.append(self.hand[search].pop(card))
                    return move
            power = 0
        return move
    def __str__(self):
        return self.name + ', ' + str(self.getCards())
class Human(Player):
    def __init__(self, name='Player'):
        Player.__init__(self, name)
    def giveWorst(self):
        while True:
            try:
                worst = input("Enter the card you want to give away (e.g., 3C): ").upper()
                if not (worst[0] in values2 and worst[1] in 'DCHS' and len(worst) == 2):
                    raise IOError
                if not worst in self.getCards():
                    raise IndexError
                if worst[0] == '2':
                    self.hand[0].remove(worst)
                    return worst
                for subhand in range(1,5):
                    rest = []
                    for card in range(len(self.hand[subhand])-1,-1,-1):
                        if self.hand[subhand][card][0] == worst[0]:
                            rest.append(self.hand[subhand].pop(card))
                    if len(rest) > 0:
                        rest.remove(worst)
                        self.addCards(rest)
                        return worst
            except IOError:
                print("You have not correctly entered a card. Please be\n\
                      sure to follow the correct format (e.g., 7D).")
            except IndexError:
                print("The card you have entered is not in your hand.")
    def give2Worst(self):
        worst = []
        print("First:")
        worst.append(self.giveWorst())
        print("Second:")
        worst.append(self.giveWorst())
        return worst
    def play(self, field):
        print("Your hand:")
        print(self.getCards())
        while True:
            try:
                move = input("Enter the card(s) you want to play (e.g., QC QD) or pass: ").upper().replace(',',' ').split(' ')
                if move == [''] or move == ['PASS']:
                    return []
                for card in move:
                    if not (card[0] in values2 and card[1] in 'DCHS' and len(card) == 2):
                        raise FormatError
                    if not card in self.getCards():
                        raise MissingError
                    if card[0] != move[0][0]:
                        raise MismatchError
                for compare in range(0,len(move)-1):
                    for contrast in range(compare+1,len(move)):
                        if move[compare] == move[contrast]:
                            raise RepeatError
                if move[0][0] != '2' and len(move) <= len(field):
                    if len(move) < len(field):
                        raise WeakError
                    if values[move[0][0]] < values[field[0][0]]:
                        raise WeakError
                self.removeCards(move)
                return move
            except FormatError:
                print("You have not correctly entered a card. Please be\nsure to follow the correct format (e.g., 7D).")
            except MissingError:
                print("A card you have entered is not in your hand.")
            except MismatchError:
                print("You cannot play cards of different values.")
            except RepeatError:
                print("Your input contains repetitions.")
            except WeakError:
                print("You must play a stronger set of cards.")

class FormatError(Exception):
    pass
class MissingError(Exception):
    pass
class MismatchError(Exception):
    pass
class RepeatError(Exception):
    pass
class WeakError(Exception):
    pass
        
class Game(object):
    def __init__(self, numplay):
        self.deck = []
        for i in values2:
            self.deck.append(i + "D")
            self.deck.append(i + "C")
            self.deck.append(i + "H")
            self.deck.append(i + "S")
        self.players = [Human()]
        for i in range(numplay - 1):
            self.players.append(Player("Computer " + str(i + 1)))
        self.president = -1
        self.vicePresident = -1
        self.viceScum = -1
        self.scum = -1
    def shuffle(self):
        for i in range(4):
            left = self.deck[:26]
            right = self.deck[26:]
            self.deck = []
            while len(left) > 0 and len(right) > 0:
                if random.choice((True, False)):
                    self.deck.append(left.pop())
                else:
                    self.deck.append(right.pop())
            self.deck = self.deck + right + left
    def round(self):
        self.shuffle()
        index = 0
        field = []
        living = self.players.copy()
        last = -1
        passes = -1
        print("Dealing cards.")
        while len(self.deck) > 0:
            dealCard = self.deck.pop()
            if dealCard == '3C' and self.president == -1:
                current = index
            self.players[index].addCard(dealCard)
            index = (index + 1) % len(self.players)
        print("Your hand:")
        print(self.players[0].getCards())
        if self.president != -1:
            time.sleep(1)
            print("President " + self.players[self.president].getName() + " and Scum " +\
                  self.players[self.scum].getName() + " exchange cards.")
            worst2 = self.players[self.president].give2Worst()
            best2 = self.players[self.scum].give2Best()
            self.players[self.president].addCards(best2)
            self.players[self.scum].addCards(worst2)
            if self.president == 0:
                print("You have been given " + str(best2))
            if self.scum == 0:
                print("You have been given " + str(worst2) + " in exchange for " + str(best2))
        if self.vicePresident != -1:
            time.sleep(1)
            print("Vice President " + self.players[self.vicePresident].getName() + \
                  " and Vice Scum " + self.players[self.viceScum].getName() + " exchange cards.")
            worst1 = self.players[self.vicePresident].giveWorst()
            best1 = self.players[self.viceScum].giveBest()
            self.players[self.vicePresident].addCard(best1)
            self.players[self.viceScum].addCard(worst1)
            if self.vicePresident == 0:
                print("You have been given " + best1)
            if self.viceScum == 0:
                print("You have been given " + worst1 + " in exchange for " + str(best1))
        if self.president != -1:
            current = self.president
        while len(living) > 1:
            info = []
            for person in range(0,len(self.players),2):
                info.append('{0:<11}:{1:<2}'.format(self.players[person].getName(),len(self.players[person].getCards())))
            for i in range(1,len(self.players),2):
                info[(i-1)//2] += ('           {0:<11}:{1:<2}'.format(self.players[i].getName(),len(self.players[i].getCards())))
            print()
            time.sleep(2)
            for line in info:
                print(line)
            if passes == 0 or last == current:
                self.deck.extend(field)
                field = []
            time.sleep(.5)
            if field == []:
                print("Field is currently empty")
            else:
                print("Current field is " + str(field))
            time.sleep(.5)
            print("It is " + living[current].getName() + "'s turn.")
            print()
            newMove = living[current].play(field)
            if newMove == []:
                print(living[current].getName() + " passes.")
                passes -= 1
                current = (current + 1) % len(living)
            else:
                print(living[current].getName() + " plays " + str(newMove))
                passes = len(living) - 1
                if living[current].getCards() == []:
                    if len(self.players) - len(living) == 0:
                        time.sleep(.5)
                        print(living[current].getName() + " has become President!")
                        self.president = self.players.index(living[current])
                    elif len(self.players) - len(living) == 1 and len(self.players) > 3:
                        time.sleep(.5)
                        print(living[current].getName() + " has become Vice President!")
                        self.vicePresident = self.players.index(living[current])
                    elif len(living) == 2 and len(self.players) > 3:
                        time.sleep(.5)
                        print(living[current].getName() + " has become Vice Scum.")
                        self.viceScum = self.players.index(living[current])
                    else:
                        time.sleep(.5)
                        print(living[current].getName() + " has become Neutral.")
                    last = -1
                    living.pop(current)
                    current = current % len(living)
                else:
                    last = current
                    current = (current + 1) % len(living)
                if newMove[0][0] == '2':
                    if last != -1:
                        current = (current - 1) % len(living)
                    field.extend(newMove)
                    newMove = []
                elif len(newMove) == 1 and len(field) == 1 and newMove[0][0] == field[0][0]:
                    time.sleep(.5)
                    print(living[current].getName() + " has been skipped!")
                    current = (current + 1) % len(living)
                elif len(newMove) == 2 and len(field) == 2 and newMove[0][0] == field[0][0]:
                    time.sleep(.5)
                    print(living[current].getName() + " and " + living[(current+1)%len(living)].getName() \
                          + " have been double-skipped!")
                    current = (current + 2) % len(living)
                self.deck.extend(field)
                field = newMove
        time.sleep(.5)
        print(living[0].getName() + " has become Scum.")
        self.scum = self.players.index(living[0])
        self.deck = self.deck + field + living[0].getCards()
gogo = True
while gogo:
    try:
        numPlayers = int(input("How many players? [3-6]: "))
        if numPlayers < 2 or numPlayers > 6:
            raise ValueError
        gogo = False
    except ValueError:
        print("Invalid input; answer must be integer between 3 and 6")
g = Game(numPlayers)
while True:
    g.round()
