import Tkinter as tk
import shutil
import os
import sys
from PIL import Image, ImageTk
import tkSimpleDialog
import tkMessageBox

window = tk.Tk()

if os.path.exists("new_tweets.txt"):
    os.remove("new_tweets.txt")
if os.path.exists("new_preprocessed.txt"):
    os.remove("new_preprocessed.txt")
if os.path.exists("twitter-out.txt"):
    os.remove("twitter-out.txt")
print("Clearing files done")


window.title("Sentiment Analysis")

window.geometry("250x150")
window.resizable(False,False)
window.configure(background="#333")


def fetchTweets():
    var = tkSimpleDialog.askstring("Search Word", "Enter keyword to fetch tweets")
    if var.startswith('#'): 
        var = "\\"+ var
        print var
        os.system('python tweet.py '+ var)
    else: os.system('python tweet.py '+ var)
    tkMessageBox.showinfo("Total Fetched Tweets", "Fetched 30 Tweets.\nView them at new_tweets.txt")

    fetchedTweetsWindow = tk.Tk()
    fetchedTweetsWindow.title("Live Fetched Tweets")
    fetchedTweetsWindow.geometry("1000x600")
    # MAX LENGTH
    max_length=0
    for line in open('new_tweets.txt'):
        if(len(line)>max_length):
            max_length=len(line)

    listBox = tk.Listbox(fetchedTweetsWindow,height=31,width=max_length+5)
    i=1
    for line in open('new_tweets.txt'):
        line=line.rstrip()
        listBox.insert(i,str(i)+": "+line)
        i+=1
    listBox.pack()
    fetchedTweetsWindow.mainloop()

def preprocess():
    os.system('python preprocess.py')
    count = 0
    f= open('new_preprocessed.txt','r')
    for line in f:
        count = count + 1
    tkMessageBox.showinfo("Preprocessing Tweets", "After preprocessing we have "+str(count)+ " tweets left. \nView them at new_preprocessed.txt")
    
    preprocessWindow = tk.Tk()
    preprocessWindow.title("Preprocessed Tweets")
    preprocessWindow.geometry("1000x600")
    # MAX LENGTH
    max_length=0
    for line in open('new_preprocessed.txt'):
        if(len(line)>max_length):
            max_length=len(line)

    listBox = tk.Listbox(preprocessWindow,height=31,width=max_length+5)
    i=1
    for line in open('new_preprocessed.txt'):
        line=line.rstrip()
        listBox.insert(i,str(i)+": "+line)
        i+=1
    listBox.pack()
    preprocessWindow.mainloop()


def runModel():
    tkMessageBox.showinfo("CNN model", "Model running....\nThis takes around 5-10mins.\nPls be patient")
    os.system('python twitter-sentiment-cnn.py --load /home/sujit_surendranath/Music/NLP/twitter-sentiment-cnn/run20190322-011848 --custom_input "this book sucks"')
    pos = 0
    neg = 0
    f= open('twitter-out.txt','r')
    for line in f:
        line = line.rstrip()
        if line == 'pos':
            pos = pos +1
        if line == "neg":
            neg = neg+1
    tkMessageBox.showinfo("Result", "Postives: "+str(pos)+"\nNegatives: "+str(neg))
    userName()

def graph():
    os.system('python graph.py')


def userName():
    from itertools import izip
    countingPositive = dict()
    with open('new_tweets.txt','r') as tweet, open('twitter-out.txt','r') as  pree:
        for x, y in izip(tweet, pree):
            sentiment = y.rstrip()
            for word in x.split(" "):
                word = word.rstrip()
                if(word.startswith('@')):
                    dictReturn = countingPositive.get(word,[0,0])
                    posCount = dictReturn[0]
                    negCount = dictReturn[1]
                    if(sentiment=='pos'):
                        posCount = posCount +1
                    if(sentiment=='neg'):
                        negCount = negCount +1
                    countingPositive[word] = [posCount,negCount]

    countWindow = tk.Tk()
    countWindow.title("Count Window")
    countWindow.geometry("800x600")
    max_length=0
    for line in open('new_tweets.txt'):
        if(len(line)>max_length):
            max_length=len(line)

    listBox = tk.Listbox(countWindow,height=21,width=max_length+5)
    i=1
    for tag in countingPositive.keys():
        value = countingPositive.get(tag)
        displayString  = str(tag) + " has Positive Tweets: "+str(value[0])+" Negative Tweets: "+str(value[1])
        listBox.insert(i,str(displayString))
        i+=1
    listBox.pack()
    button4 = tk.Button(countWindow, text='Plot Graph',width=15, command=graph, background = 'black', foreground = "white", highlightthickness=0, bd=0) 
    button4.pack() 
    countWindow.mainloop()


button1 = tk.Button(window, text='Fetch Tweets',width=15,command=fetchTweets,background = 'white', foreground = "black", highlightthickness=0, bd=0) 
# button1.grid(row=0, column=2) 
button1.pack()


button2 = tk.Button(window, text='Preprocess tweets', width=15, command=preprocess, background = 'black', foreground = "white", highlightthickness=0, bd=0) 
button2.pack()


button3 = tk.Button(window, text='Run Model', width=15, command=runModel, background = 'white', foreground = "black",highlightthickness=0, bd =0) 
button3.pack()





pathlabel = tk.Label(window)
# pathlabel.grid()

window.mainloop()
