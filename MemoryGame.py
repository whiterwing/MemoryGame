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
    '''
    This is a class to hold variables in so I don't have to declare globes.
    '''
    difficulty = 0
    choices = list()
    remainingTiles = 0
    root = None
    
    def pre_game(self, master):
        self.difficulty = Difficulty_menu(master)
    
    def start_game(self, master):
        #Since Play.check_choice is ran from a tile, this needs to be here to call Play.end_game from check_choice.
        self.play = Play(master)


class Tile():
    '''
    Each one of the game Tiles is it's own object. I did it this way, so I can create tiles as needed to fill the board.
    '''
    def __init__(self, master, text, row, column):
        self.text = text
        self.row = row
        self.column = column
        
        self.master = master
        self.tileFrame = TK.Frame(master)
        self.tileFrame.grid(row=self.row,column=self.column,padx=1,pady=1)
        
        self.button = TK.Button(self.tileFrame, text=self.text, height=1, width=1, bg="Black", command=self.pressed)
        self.button.pack()
        
    def pressed(self):
        #set the background to white so the player can see the number.
        self.button['bg'] = "White"
        #disables the button so the player can't just click the button twice to add the same tile to Variables.choices
        self.button['state'] = "disabled"
        
        #print (self.text)
        
        Variables.choices.append(self)
        
        if len(Variables.choices) == 2:
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
            
        random.shuffle(self.gameArray)
        
        #creates a tile for each item in the gameArray.
        #breaks the tiles into x,y pos. 5 tiles per row.
        for i in range(len(self.gameArray)):
            row = i//5
            column = i%5
            text=self.gameArray[i]
            
            #creates the Tile object and assigns it a vaule, and grid location.
            #creating the tile, then adding it to an array.
            newTile = Tile(self.gameBoard, text, row, column)
            self.gameTiles.append(newTile)
            
            Variables.remainingTiles = len(self.gameTiles)
            
            #print(newTile.text, newTile.row, newTile.column)
            
    def check_choice(self):
        time.sleep(1) #leaves both tiles visable for the player to see for a second.
        #Variables.remainingTiles = 0
        
        choices = Variables.choices
        
        #if the tiles don't match, hide the value, and let the player click it again.
        #otherwise clear the choices list, and decrement the remainingTiles counter.
        if choices[0].text != choices[1].text:
            choices[0].button['bg'] = "Black"
            choices[0].button['state'] = "normal"
            choices[1].button['bg'] = "Black"
            choices[1].button['state'] = "normal"
            Variables.choices = list()
        else:
            Variables.choices = list()
            Variables.remainingTiles -=2

        #if there are no tiles left, end the game.
        if Variables.remainingTiles == 0:
            Variables.play.end_game()
            
    def end_game(self):
        #destroys all the tile objects.
        for tile in self.gameTiles:
            tile.finish()
        
        #displays a finish message.
        self.label = TK.Label(self.gameBoard, text = "!!!YOU WON!!!")
        self.label.pack(fill=TK.BOTH)

        #creates a pop up to ask if the user wants to play again, returns a bool.
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