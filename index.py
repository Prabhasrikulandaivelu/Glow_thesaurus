from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import json
import pyttsx3
from difflib import get_close_matches
import PyPDF2
from translate import Translator



import os
from textblob import TextBlob

engine = pyttsx3.init()


def speaknow():
    text = textarea.get(1.0,END)
    Gender = cmb.get()
    Speed = spd.get()
    voices = engine.getProperty('voices')

    def Setvoice():

        if Gender == 'Male':
            engine.setProperty('voice', voices[0].id)
            engine.say(text)
            engine.runAndWait()
        else:
            engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()

    if text:
        if Speed == "Fast":
            engine.setProperty('rate', 250)
            Setvoice()
        elif Speed == "Normal":
            engine.setProperty('rate', 150)
            Setvoice()
        else:
            engine.setProperty('rate', 60)
            Setvoice()


def download():
    text = textarea.get(1.0, END)
    Gender = cmb.get()
    Speed = spd.get()
    voices = engine.getProperty('voices')

    def Setvoice():

        if Gender == 'Male':
            engine.setProperty('voice', voices[0].id)
            path=filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text, 'text.mp3')
            engine.runAndWait()
        else:
            engine.setProperty('voice', voices[1].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text, 'text.mp3')
            engine.runAndWait()

    if text:
        if Speed == "Fast":
            engine.setProperty('rate', 250)
            Setvoice()
        elif Speed == "Normal":
            engine.setProperty('rate', 150)
            Setvoice()
        else:
            engine.setProperty('rate', 60)
            Setvoice()


def clearAll():
    # whole content of text entry area is deleted
    word1_field.delete(0, END)
    word2_field.delete(0, END)

def clear():
    textarea.config(state=NORMAL)
    enterwordentry.delete(0, END)
    textarea.delete(1.0, END)
    textarea.config(state=DISABLED)

def correction():

    input_word = word1_field.get()

    blob_obj = TextBlob(input_word)

    corrected_word = str(blob_obj.correct())

    word2_field.insert(10, corrected_word)

def search():
    data = json.load(open('data.json')) #loads the data.json file to the program
    word = enterwordentry.get()# insert the word in the entry box

    word = word.lower() # we type in upper case it will automatically convert to lower case and display the meaning

    if word in data: # check if the word present in the data.json file
        meaning = data[word]

        textarea.config(state=NORMAL)
        textarea.delete(1.0, END)
        for item in meaning: # for displaying the meaning in text area
            textarea.insert(END, u'\u2022' + item + '\n\n')

        textarea.config(state=DISABLED)

    elif len(get_close_matches(word, data.keys())) > 0: # if we type the wrong spelling  then this will show the close matches

        close_match = get_close_matches(word, data.keys())[0]

        res = messagebox.askyesno('Confirm', 'Did you mean ' + close_match + ' instead?') # confirm window

        if res == True:# if there is crt spelling then this will get executed
            enterwordentry.delete(0,END)
            enterwordentry.insert(END,close_match)


            meaning = data[close_match] # inserting the closematch meaning to the text area
            textarea.delete(1.0, END)
            textarea.config(state=NORMAL)
            for item in close_match:
                textarea.insert(END, item)

            textarea.config(state=DISABLED)

        else:
            textarea.delete(1.0, END)
            messagebox.showinfo('Information', 'Please type a correct word')
            enterwordentry.delete(0, END)

    else: # if u couldn't find the word then this will display the error message
        messagebox.showerror('Error', 'The word doesnt exist.Please double check it.')
        enterwordentry.delete(0, END)
        


root = Tk()
root.title("GLOW THESAURUS")
root.geometry("1000x680+100+30")
root.resizable(False, False)
root.configure(bg="#305065")


# icon
image_icon = PhotoImage(file="speak.png")
root.iconphoto(False, image_icon)


# top frame
Topframe = Frame(root, bg="white", width=1000, height=100)
Topframe.place(x=0, y=0)

Logo = PhotoImage(file="speaker logo.png")
Label(Topframe, image=Logo, bg="white" ).place(x=370, y=5)
Label(Topframe, text=" GLOW THESAURUS", font="arial 20 bold", bg="orange", fg="black").place(x=100, y=30)
Logos = PhotoImage(file="pra.png.png")
Label(Topframe, image=Logos,height=100,width=100,bg="white").place( y=5)


enterwordLabel = Label(root, text='Enter Word', font=('castellar', 20, 'bold'), fg='red3', bg='whitesmoke')
enterwordLabel.place(x=100, y=110)
enterwordentry = Entry(root, font=('arial', 23, 'bold'), bd=8, relief=GROOVE, justify=CENTER)
enterwordentry.place(x=20, y=160)
enterwordentry.focus_set()

searchimage = PhotoImage(file='search (1).png.')
searchButton = Button(root, image=searchimage, bg='whitesmoke',  cursor='hand2',command=search,bd=4)
searchButton.place(x=400, y=150)

meaninglabel = Label(root, text='Meaning', font=('castellar', 29, 'bold'), fg='red3', bg='whitesmoke')
meaninglabel.place(x=100, y=230)

clearimage=PhotoImage(file='clear (1).png')
clearbutton= Button(root, image=clearimage, bg='whitesmoke', command=clear, cursor='hand2',bd=0)
clearbutton.place(x=250,y=610)

textarea = Text(root, font="robote", bg="light pink", bd=8, relief=GROOVE, wrap=WORD)
textarea.place(x=5, y=300, width=500, height=300)
label1 = Label(root, text="Input Word", font=('castellar', 15, 'bold'), fg='red3', bg='whitesmoke')

label2 = Label(root, text="Corrected Word", font=('castellar', 15, 'bold'), fg='red3', bg='whitesmoke')

label1.place(x=550, y=355)

label2.place(x=520, y=460)

word1_field = Entry(root, font=('arial', 10, 'bold'), bd=8, relief=GROOVE, justify=CENTER)

word2_field = Entry(root, font=('arial', 10, 'bold'), bd=8, relief=GROOVE, justify=CENTER)

word1_field.place(x=760, y=353)


word2_field.place(x=760, y=460)
button1 = Button(root, text="Correction", bg="red", fg="black",font=('arial',12,'bold'), command=correction,cursor='hand2')

button1.place(x=793, y=400)

button2 = Button(root, text="Clear", bg="red",fg="black",font=('arial',12,'bold'), command=clearAll,cursor='hand2')
button2.place(x=805, y=510)

l1 = Label(root, text="SELECT YOUR OPTIONS", font="bold", bg="light green")
l1.place(x=530, y=130)

l2 = Label(root, text="Voice", font="bold", bg="light green")
l2.place(x=575, y=175)

l3 = Label(root, text="Speed", font="bold", bg="light green")
l3.place(x=738, y=175)
Gender = ["Male", "Female"]
cmb = ttk.Combobox(root, value=Gender, width=20,cursor='hand2')
cmb.place(x=530, y=210)
cmb.current(0)

Speed = ["Normal", "Fast", "Slow"]
spd = ttk.Combobox(root, value=Speed, width=20,cursor='hand2')
spd.place(x=700, y=210)
spd.current(0)

imageicon = PhotoImage(file="speak.png")
btn = Button(root, text="Speak", compound=LEFT, image=imageicon, width=120, height=50, font="arial 14 bold",command=speaknow,cursor='hand2')
btn.place(x=530, y=270)

imageicon1 = PhotoImage(file="download.png")
save = Button(root, text="Save", compound=LEFT, image=imageicon1, width=120, height=50, font="arial 14 bold",command=download,cursor='hand2',bg="orange")
save.place(x=700, y=270)


def open_win():
   new= Toplevel(root)
   new.geometry("1000x680+100+30")
   new.resizable(FALSE,FALSE)

   new.title("pdf to speech")
   new.config(bg="#305065")


   #Create a Label in New window
   page1 = Label(new, text=" Enter starting page number",font=('Playfair Display',24,'bold'),bg='light green',fg='black',border=4)
   startingpagenumber = Entry(new, font=('arial', 10, 'bold'), bd=13, relief=GROOVE, justify=CENTER)
   page1.place(x=50,y=60)
   startingpagenumber.place(x=520,y=60)

   label = Label(new, text="Select the book you want to read.",font=('Playfair Display',24,'bold'),bg='light green',fg='black')
   label.place(x=50,y=200)

   InputLanguageChoice = StringVar()
   TranslateLanguageChoice = StringVar()
   LanguageChoices = {'Hindi', 'English', 'French', 'German', 'Spanish'}
   InputLanguageChoice.set('English')
   TranslateLanguageChoice.set('Hindi')

   def Translate():
       translator = Translator(from_lang=InputLanguageChoice.get(), to_lang=TranslateLanguageChoice.get())
       Translation = translator.translate(TextVar.get())
       OutputVar.set(Translation)
       # choice for input language

   Label(new, text="TRANSLATOR", font=('Playfair Display',40, 'bold'), fg='black').place(x=200, y=300)
   InputLanguageChoiceMenu = OptionMenu(new, InputLanguageChoice, *LanguageChoices)
   Label(new, text="Choose a Language",font=('Playfair Display',20,'bold'),bg='light green',fg='black').place(x=50,y=400)
   InputLanguageChoiceMenu.place(x=100,y=450)

   # choice in which the language is to be translated
   NewLanguageChoiceMenu = OptionMenu(new, TranslateLanguageChoice, *LanguageChoices)
   Label(new, text="Translated Language",font=('Playfair Display',20,'bold'),bg='light green',fg='black').place(x=400,y=400)
   NewLanguageChoiceMenu.place(x=480,y=450)
   Label(new, text="Enter Text",font=('Playfair Display',18),bg='light green',fg='black').place(x=50,y=500)
   TextVar = StringVar()
   TextBox = Entry(new, textvariable=TextVar,font=('arial', 10, 'bold'), bd=8, relief=GROOVE, justify=CENTER).place(x=170,y=500)

   Label(new, text="Output Text",font=('Playfair Display',18),bg='light green',fg='black').place(x=400,y=500)
   OutputVar = StringVar()
   TextBox = Entry(new, textvariable=OutputVar,font=('arial', 10, 'bold'), bd=8, relief=GROOVE, justify=CENTER).place(x=550,y=500)

   # Button for calling function
   B = Button(new, text="Translate", command=Translate, font=('arial', 10, 'bold'), bd=8, relief=GROOVE, justify=CENTER).place(x=330,y=560)

   def file():
       path = filedialog.askopenfilename()
       book = open(path, 'rb')
       pdfreader = PyPDF2.PdfFileReader(book)
       pages = pdfreader.numPages
       speaker = pyttsx3.init()

       for i in range(int(startingpagenumber.get()), pages):
           page = pdfreader.getPage(i)
           txt = page.extractText()
           speaker.say(txt)
           speaker.runAndWait()

   B = Button(new, text="Choose  the Book",font=('Playfair Display',15,'bold'),bg='light green',fg='black', command=file)
   B.place(x=600,y=200)


#Create a label
Label(root, text= "CONVERT PDF TO SPEECH", bg='gold', font= (' bold')).place(x=600,y=560)
#Create a button to open a New Window
ttk.Button(root, text="click me", command=open_win).place(x=710,y=600)



root.mainloop()





