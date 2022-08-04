# -*- coding: utf-8 -*-
"""
Memory Puzzle Game

Difficulty selector
Array of tiles, each tile needs to be in twice
display tiles for 5 seconds
show tile on click
after second tile is clicked:
    if tiles match increase score keep tiles shown
    else decrease score hide tiles.
"""

import random
import tkinter as TK
import time

class Variables():
    difficulty = 0
    choices = list()
    remainingTiles = 0
    root = None
    
    def pre_game(self, master):
        self.difficulty = Difficulty_menu(master)
    
    def start_game(self, master):
        self.play = Play(master)


class Tile():
    def __init__(self, master, text, row, column):
        self.text = text
        self.row = row
        self.column = column
        
        self.master = master
        self.tileFrame = TK.Frame(master)
        self.tileFrame.grid(row=self.row,column=self.column)
        
        self.button = TK.Button(self.tileFrame, text=self.text, bg="Black", command=self.pressed)
        self.button.pack(expand=True)
        
    def pressed(self):
        self.button['bg'] = "White"
        print (self.text)
        if len(Variables.choices) == 0:
            Variables.choices.append(self)
        else:
            Variables.choices.append(self)
            Play.check_choice(self)
            
    def finish(self):
        self.tileFrame.destroy()


class Play():
    def __init__(self,master):
        self.master = master
        self.gameBoard = TK.Frame(self.master)
        self.gameBoard.pack(fill=TK.BOTH)
    
        self.gameArray = list()  #creates the list to be shuffled.
        self.gameTiles = list() #creates the list for the tiles.
        print(Variables.difficulty)
        
        self.make_game_board()
        
    def make_game_board(self):
        for num in range(1,Variables.difficulty+1): #difficulty selector: easy=5;med=10;hard=20
        #append each number twice since you have to match the tiles.
            self.gameArray.append(num)
            self.gameArray.append(num)
            
        #shuffle's the array twice to make it a little more random.
        shuffleCount = 2
        while shuffleCount:
            random.shuffle(self.gameArray)
            shuffleCount -= 1
        
        #creates a tile for each item in the gameArray.
        #breaks the tiles into x,y pos. 5 tiles per row.
        for i in range(len(self.gameArray)):
            row = i//5
            column = i%5
            text=self.gameArray[i]
            
            #creates the Tile object and assigns it a vaule, and grid location.
            #creating the tile, then adding it to array for testing reasons.
            newTile = Tile(self.gameBoard, text, row, column)
            self.gameTiles.append(newTile)
            
            Variables.remainingTiles = len(self.gameTiles)
            print(newTile.text, newTile.row, newTile.column)
            
    def check_choice(self):
        time.sleep(1)
        #Variables.remainingTiles = 0
        
        choices = Variables.choices
        if choices[0].text != choices[1].text:
            choices[0].button['bg'] = "Black"
            choices[1].button['bg'] = "Black"
            Variables.choices = list()
        else:
            choices[0].button['state'] = "disabled"
            choices[1].button['state'] = "disabled"
            Variables.choices = list()
            Variables.remainingTiles -=2

        if Variables.remainingTiles == 0:
            Variables.play.endGame()
            
    def endGame(self):
        for tile in self.gameTiles:
            tile.finish()
        
        self.label = TK.Label(self.gameBoard, text = "!!!YOU WIN!!!")
        self.label.pack(fill=TK.BOTH)

        self.alertBox = TK.messagebox.askyesno("Continue", "Do you want to play again?")
        
        self.gameBoard.destroy()
        
        if self.alertBox:
            Difficulty_menu(self.master)
        else:
            Variables.root.destroy()


class Window():
    def __init__(self, master):
        '''
            Main window for the memory game. calls the difficulty menu to start the app.
        '''
        self.main=TK.Frame(master)
        self.main.pack(fill=TK.BOTH)
        
        self.difficulty = Variables.pre_game(Variables, self.main)
        
        
class Difficulty_menu():
    def __init__(self, master):
        '''
            creates the difficulty menu for the game. Let's the player choose the following options:
                
            easy = 10 tiles
            medium = 20 tiles
            hard = 40 tiles
        '''
        print("Difficulty_menu")
        self.master = master
        self.menu=TK.Frame(self.master)
        self.menu.pack()
        
        self.easy_button = TK.Button(self.menu, text="Easy", width= 20, pady=5, command=lambda: self.start_game(5))
        self.easy_button.pack()
        
        self.med_button = TK.Button(self.menu, text="Medium", width= 20, pady=5, command=lambda: self.start_game(10))
        self.med_button.pack()
        
        self.hard_button = TK.Button(self.menu, text="Hard", width= 20, pady=5, command=lambda: self.start_game(20))
        self.hard_button.pack()
        
    def start_game(self, y):
        Variables.difficulty = y
        Variables.start_game(Variables, self.master)
        self.menu.destroy()
        
        
root = TK.Tk()
root.title("Memory")
root.geometry("300x300")
Variables.root = root
main = Window(root)
root.mainloop()