"""UNO Simulator

This program is meant to simulate the trademarked card game UNO(TM).

After this program is completed and debugged, it will be used to train and test an AI for winning at UNO.

This program is designed for the standard 108 card version of UNO, including:
    -19 blue number cards
    -2 blue reverse cards
    -2 blue skip cards
    -2 blue draw 2 cards
    -19 red number cards
    -2 red reverse cards
    -2 red skip cards
    -2 red draw 2 cards
    -19 green number cards
    -2 green reverse cards
    -2 green skip cards
    -2 green draw 2 cards
    -19 yellow number cards
    -2 yellow reverse cards
    -2 yellow skip cards
    -2 yellow draw 2 cards
    -4 wild cards
    -4 wild draw 4 cards
"""

import random

class Player:
    def __init__(self,number,name=None):
        self.number=number
        self.name=name
        self.hand=[]
    
    def addToHand(self,card):
        self.hand.append(card)
        
    def evaluateHand(self,card): # I am considering methods to organize playable cards in a certain order
        playableCards={}
        index=1
        for myCard in self.hand:
            if card[1]=="draw 2":
                if myCard[1]=="draw 2":
                    playableCards[index]=myCard
            elif card[1]=="draw 4":
                if (myCard[1]=="draw 2" and myCard[0]==card[0]) or myCard[1]=="draw 4":
                    playableCards[index]=myCard
            else:
                if myCard[0]==card[0] or myCard[1]==card[1] or myCard[0]=="wild":
                    playableCards[index]=card
            index+=1
        return playableCards
    
    def removeFromHand(self,card):
        self.hand.remove(card)
    
    def getHand(self):
        return self.hand
        
def overhandShuffle(deck): #This is meant to be simulate an ideal overhand shuffle
    split1 = deck[:len(deck)//2]
    split2 = deck[len(deck)//2:]
    newDeck = []
    for i in range(len(split1)):
        newDeck.append(split1[i])
        newDeck.append(split2[i])
    if len(split1)<len(split2):
        newDeck.append(split2[-1])
    newDeck[:len(newDeck)//2],newDeck[len(newDeck)//2:] = newDeck[len(newDeck)//2:],newDeck[:len(newDeck)//2]
    return newDeck

#This is my implementation if I were to use a singly-linked list to represent the player order
class SinglyLinkedList:
    class Node:
        def __init__(self,value,nxt=None):
            self.value=value
            self.next=nxt
        
        def getNext(self):
            return self.next
        
        def setNext(self,nxt):
            self.next=nxt
    
    def __init__(self,nodeVals):
        nodes=[]
        for val in nodeVals:
            nodes.append(SinglyLinkedList.Node(val))
        for i in range(len(nodes)-1):
            nodes[i].next=nodes[i+1]
        nodes[-1].next=nodes[0]
        self.cursor=nodes[0]
    
    def __iter__(self):
        node = self.cursor
        while node.next != self.cursor:
            yield node
            node = node.next
        yield node
    
    def reverse(self):
        prevNode = self.cursor
        curNode = self.cursor.next
        while curNode!=self.cursor:
            nextNode = curNode.next
            curNode.next=prevNode
            prevNode=curNode
            curNode=nextNode
        curNode.next=prevNode
    
    def getCursor(self):
        return self.cursor
    
    def moveCursor(self):
        self.cursor=self.cursor.next
        return self.cursor

#This is my implementation if I were to use a doubly-linked list to represent the player order
class DoublyLinkedList:
    class Node:
        def __init__(self,value,left=None,right=None):
            self.value=value
            self.left=left
            self.right=right
            
        def getNext(self,direction):
            if direction=="0":
                return self.left
            elif direction=="1":
                return self.right
            
        def setLeft(self,left):
            self.left=left
            
        def setRight(self,right):
            self.right=right
        
    def __init__(self,nodeVals):
        nodes=[]
        for val in nodeVals:
            nodes.append(DoublyLinkedList.Node(val))
        for i in range(len(nodes)-1):
            nodes[i].left=nodes[i+1]
            nodes[i].right=nodes[i-1]
            #print(nodes[i-1].value,nodes[i].value,nodes[i+1].value)
        nodes[-1].left=nodes[0]
        nodes[-1].right=nodes[-2]
        #print(nodes[-1].right.value,nodes[-1].value,nodes[-1].left.value)
        self.cursor = nodes[0]
        self.direction = 0
        
    def __iter__(self):
        node = self.cursor
        if self.direction:
            while node.right != self.cursor:
                yield node
                node = node.right
            yield node
        else:
            while node.left != self.cursor:
                yield node
                node = node.left
            yield node
    
    def reverse(self):
        self.direction = not self.direction
    
    def getCursor(self):
        return self.cursor
    
    def moveCursor(self):
        if self.direction:
            self.cursor = self.cursor.right
        else:
            self.cursor = self.cursor.left

drawPile = [('blue','0'),('blue','1'),('blue','1'),('blue','2'),('blue','2'),('blue','3'),('blue','3'),('blue','4'),('blue','4'),('blue','5'),('blue','5'),('blue','6'),('blue','6'),('blue','7'),('blue','7'),('blue','8'),('blue','8'),('blue','9'),('blue','9'),('blue','draw 2'),('blue','draw 2'),('blue','reverse'),('blue','reverse'),('blue','skip'),('blue','skip'),
        ('green','0'),('green','1'),('green','1'),('green','2'),('green','2'),('green','3'),('green','3'),('green','4'),('green','4'),('green','5'),('green','5'),('green','6'),('green','6'),('green','7'),('green','7'),('green','8'),('green','8'),('green','9'),('green','9'),('green','draw 2'),('green','draw 2'),('green','reverse'),('green','reverse'),('green','skip'),('green','skip'),
        ('red','0'),('red','1'),('red','1'),('red','2'),('red','2'),('red','3'),('red','3'),('red','4'),('red','4'),('red','5'),('red','5'),('red','6'),('red','6'),('red','7'),('red','7'),('red','8'),('red','8'),('red','9'),('red','9'),('red','draw 2'),('red','draw 2'),('red','reverse'),('red','reverse'),('red','skip'),('red','skip'),
        ('yellow','0'),('yellow','1'),('yellow','1'),('yellow','2'),('yellow','2'),('yellow','3'),('yellow','3'),('yellow','4'),('yellow','4'),('yellow','5'),('yellow','5'),('yellow','6'),('yellow','6'),('yellow','7'),('yellow','7'),('yellow','8'),('yellow','8'),('yellow','9'),('yellow','9'),('yellow','draw 2'),('yellow','draw 2'),('yellow','reverse'),('yellow','reverse'),('yellow','skip'),('yellow','skip'),
        ('wild','pick color'),('wild','pick color'),('wild','pick color'),('wild','pick color'),('wild','draw 4'),('wild','draw 4'),('wild','draw 4'),('wild','draw 4')
        ]
random.shuffle(drawPile)
discardPile = []

#Player setup
playerCountValid=0
while not playerCountValid:
    playerCount = int(input("Please input number of players: "))
    if playerCount<2 or playerCount>10:
        print("Error: number of players must be between 2 and 10 (inclusive)\n")
    else:
        playerCountValid=1
playerList = []
for i in range(playerCount):
    name = input("Player "+str(i+1)+", please enter your name: ")
    playerList.append(Player(i+1,name))
playerOrder = SinglyLinkedList(playerList)
#playerOrder = DoublyLinkedList(playerList)

#Deal cards to all players
for i in range(7):
    for node in playerOrder:
        node.value.addToHand(drawPile.pop())

##This is for debugging purposes
# for node in playerOrder:
#     print(node.value.getHand())

#First discard
discardPile.append(drawPile.pop())
#If first card is a draw 4, return card to the deck and draw new card
while discardPile[0][1]=="draw 4":
    drawPile.insert(discardPile.pop(),random.randint(0,len(drawPile)))
    discardPile.append(drawPile.pop())
if discardPile[0][1]=="pick color":
    selectColorFlag=1
    while selectColorFlag:
        activeColor = input("Select color (red, blue, green or yellow): ")
        if activeColor in ['red','blue','green','yellow']:
            selectColorFlag=0
else:
    activeColor = discardPile[0][0]
activeNumber = discardPile[0][1]
if discardPile[0][1]=="reverse":
    print("Reverse")
    playerOrder.reverse()
if discardPile[0][1]=="skip":
    print("\nPlayer "+playerOrder.cursor.value.number+"'s turn skipped\n")
    playerOrder.moveCursor()

drawCount = 0 #If a draw 2 or draw 4 is played, drawCount is increased by that amount
                # and is reset once cards are finally drawn

noWin = True
while noWin:
    playTurn = 1
    currentPlayer = playerOrder.cursor.value
    print("Player "+currentPlayer.number+"'s turn: "+currentPlayer.name)
    for card in currentPlayer.getHand(): #Display current player's hand
        print(card+"  ")
    playableCards = currentPlayer.evaluateHand((activeColor,activeNumber)) #Display current player's playable hand
    
    #If draw 2 or draw 4 has been played or chained and you have no cards to resist
    #then you must draw the number of cards and skip a turn
    if drawCount!=0 and len(playableCards)==0:
        print("Drawing "+drawCount+" cards...")
        for i in range(drawCount):
            currentPlayer.addToHand(drawPile.pop())
            if len(drawPile)==0:
                print("Shuffling deck...")
                lastDiscard = discardPile.pop()
                drawPile = overhandShuffle(discardPile)
                discardPile = lastDiscard
        drawCount = 0
        playTurn = 0

    if playTurn:
        while len(playableCards)==0: #If no playable cards, then keep drawing until you get one
            print("No playable cards. Drawing card...")
            currentPlayer.addToHand(drawPile.pop())
            if len(drawPile)==0:
                print("Shuffling deck...")
                lastDiscard = discardPile.pop()
                drawPile = overhandShuffle(discardPile)
                discardPile = lastDiscard
            playableCards = currentPlayer.evaluateHand((activeColor,activeNumber))
       
        selectCardFlag = 1
        while selectCardFlag: # Keep looping until a valid selection is made
            print("Current Active Card: ("+activeColor+", "+activeNumber+")\n")
            for key in playableCards:
                print(key+": "+playableCards[key]+"\n")
            selection=int(input("Input number for card to play: "))
            if selection>=1 or selection<=len(playableCards):
                selectCardFlag = 0
            else:
                print("Error. Invalid input\n\n")
        
        selectedCard = currentPlayer.removeFromHand(playableCards[selection])
        if selectedCard[0]=="wild": #If card is wild, player must decide what color it will represent
            selectColorFlag=1
            while selectColorFlag: # Keep looping until a valid selection is made
                activeColor = input("Select color (red, blue, green or yellow): ")
                if activeColor in ['red','blue','green','yellow']:
                    selectColorFlag=0
        else:
            activeColor = selectedCard[0]
        activeNumber = selectedCard[1]
        
        if activeNumber=="draw 2":
            print("Draw 2")
            drawCount+=2
        elif activeNumber=="draw 4":
            print("Draw 4")
            drawCount+=4
        if activeNumber=="reverse":
            print("Reverse")
            playerOrder.reverse()
        elif activeNumber=="skip":
            nextPlayerNode = playerOrder.cursor.getNext()
            print("\nPlayer "+nextPlayerNode.value.number+"'s turn skipped\n")
            playerOrder.moveCursor()
        discardPile.append(selectedCard)
    playerOrder.moveCursor()
