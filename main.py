from tkinter import *
from tkinter import messagebox
from string import ascii_uppercase
from PIL import Image, ImageTk
import glob
import os
import random

class Hangman:
    def __init__(self,tkWindow,wordfilePath,delimiter,imagesPath,enable_color_keyboard=True):
        self.window=tkWindow
        self.window.bind("<Key>",self.keyboard)
        self.filePath=wordfilePath
        self.delimiter=delimiter
        self.photosPath=imagesPath
        self.wordList=self.get_words()
        self.photos=self.get_photos()
        self.totalGuess=len(self.photos)-1
        self.winstreakCount=0
        self.guess_number=0
        self.create_main_ui(enable_color_keyboard)
        self.create_new_game()


    def create_main_ui(self,enableColors:bool):
        colors=['Beige','peachpuff','plum','Cornsilk','AliceBlue','cyan','pink']
        for n,letter in enumerate(ascii_uppercase):
            colorindex=random.randint(0,len(colors)-1)
            bgcolor='white'
            if enableColors:
                bgcolor=colors[colorindex]
            Button(self.window,text=letter,bg=bgcolor,command=lambda letter=letter:self.guess(letter),font=("Helevetica 15"),width=5).grid(row=1+n//9,column=n%9,sticky='NSEW',padx=2)
        n+=1
        Button(self.window,text='New Game',command=self.create_new_game,font=("Arial 12 bold"),bg='green').grid(row=1+n//9,column=n%9,sticky='NSEW')
        self.label_word=StringVar()
        Label(self.window,textvariable=self.label_word,font=("Consolas 18 bold")).grid(row=0,column=5,columnspan=6,padx=10)
        self.guessleftvar=StringVar()
        self.guessleftvar.set(f'Guess Remaining:{self.totalGuess}')
        Label(self.window,textvariable=self.guessleftvar,bg='plum',font=("Arial 10 bold")).grid(row=n,column=0,padx=2,sticky='WENS')
        self.winstreakVar=StringVar()
        self.winstreakVar.set(f'Winstreak:{self.winstreakCount}')
        Label(self.window,textvariable=self.winstreakVar,bg='lime',font=("Arial 10 bold")).grid(row=n+1,column=0,padx=2,sticky='WENS')

    def create_new_game(self):
        self.guess_number=0
        self.image_label=Label(self.window)
        self.image_label.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
        image_pil=Image.open(self.photos[0])
        image=ImageTk.PhotoImage(image_pil)
        self.image_label.config(image=image)
        self.image_label.image=image
        self.current_word=random.choice(self.wordList)
        self.current_word=self.current_word.upper()
        self.current_word_with_spaces=" ".join(self.current_word)
        self.label_word.set(" ".join("_"*len(self.current_word)))

    def guess(self,letter):
        if self.guess_number<self.totalGuess:
            text=list(self.current_word_with_spaces)
            guessed=list(self.label_word.get())
            if self.current_word_with_spaces.count(letter)>0:
                for index,alphabets in enumerate(text):
                    if alphabets==letter:
                        guessed[index]=letter
                    self.label_word.set("".join(guessed))
                    if self.label_word.get()==self.current_word_with_spaces:
                        returnval=messagebox.askquestion(f'Winner',f'You Won!!!\n Continue to new Round?')
                        self.winstreakCount+=1
                        winstreaktext=f'Winstreak:{self.winstreakCount}'
                        self.winstreakVar.set(winstreaktext)
                        if returnval=='yes':
                            self.create_new_game()
                        else:
                            self.window.destroy()
            else:
                self.guess_number+=1
                image_pil=Image.open(self.photos[self.guess_number])
                image=ImageTk.PhotoImage(image_pil)
                self.image_label.config(image=image)
                self.image_label.image=image
                guess_remain_text=f'Guess Remaining: {self.totalGuess-self.guess_number}'
                self.guessleftvar.set(guess_remain_text)
        else:
            returnval=messagebox.askquestion(f'Play Again?',f'The correct word was:{self.current_word}\nPlay Again?')
            if returnval=='yes':
                self.create_new_game()
            else:
                self.window.destroy()


    def get_words(self):
        with open(self.filePath,'r',encoding='utf-8') as f:
            words=f.read()
            wordlist=words.split(self.delimiter)
            if '' in wordlist:
                wordlist.remove('')
            return wordlist
    def get_photos(self):
        imageNames=sorted(os.listdir(self.photosPath))
        images=[os.path.join(self.photosPath,name) for name in imageNames]
        photosList=images
        return photosList

    def keyboard(self, event):
        #allowing the keyboard enter stroke to make a guess
        letter=event.char.upper()
        if letter in ascii_uppercase:
            self.guess(letter)


if __name__=='__main__':
    window=Tk()
    window.title('Hangman')
    filePath='./random_words.txt'
    delimiter=';'
    imagesPath='./resources/stages'
    hg=Hangman(window,filePath,delimiter,imagesPath,enable_color_keyboard=False)
    window.mainloop()
