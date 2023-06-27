from tkinter import *
from PIL import ImageTk

root = Tk()
root.title("First Page")
root.geometry("810x810+50+0")
root.resizable(0,0)

# import image background
bgImage = ImageTk.PhotoImage(file="bgImage.png")
bgLebel = Label(root, image=bgImage)
bgLebel.place(x=0,y=0)

heading = Label(root, text='Finate Automata', font=('Roboto', 23,'bold'), bg='white')
heading.place(x=290, y=180)



root.mainloop()