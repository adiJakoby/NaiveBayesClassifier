from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
from tkFileDialog import askdirectory
import os
import tkMessageBox
import build as builder


class Calculator:

    def __init__(self, master):

        self.master = master
        master.title("Naive Bayes Classifier")
        master.geometry("450x300")

        self.directory_path_text = Entry(master)
        self.directory_path_label = Label(master, text="Directory Path")

        def open_dialog():
            directoryPath = askdirectory()
            self.directory_path_text.delete(0, END)
            self.directory_path_text.insert(0, directoryPath)

        self.bins_label = Label(master, text="Discretization Bins")
        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.browse_button = Button(master, text="Browse", command=open_dialog)


        self.build_button = Button(master, text="Build", command=lambda: self.checkValidate())
        self.classify_button = Button(master, text="Classify", command=lambda: self.update("reset"))

        # LAYOUT

        self.directory_path_label.grid(row=2, column=0, sticky=W)
        self.directory_path_text.grid(row=2, column=1, columnspan=3, sticky=E)
        self.browse_button.grid(row=2, column=4)

        self.bins_label.grid(row=4, column=0)
        self.entry.grid(row=4, column=1, columnspan=3, sticky=W+E)

        self.build_button.grid(row=6, column=1)
        self.classify_button.grid(row=8, column=1)

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def build(self):
        builderClass = builder.builder()
        trainData = builder.builder.startBuild(builderClass, self.directory_path_text.get(), self.entered_number)
        print trainData
        tkMessageBox.showinfo("Naive Bayes Classifier", "Building classifier using train-set is done!")


    def checkValidate(self):
        bins = False
        structure = False
        train = False
        test = False

        if self.entry.get() != "":
            bins = True

        for file in os.listdir(self.directory_path_text.get()):
            if "Structure.txt" in file:
                structure = True
            if "train.csv" in file:
                train = True
            if "test.csv" in file:
                test = True

        if(structure == False):
            tkMessageBox.showinfo("Naive Bayes Classifier", "The file 'Structure.txt' is missing")

        if(train == False):
            tkMessageBox.showinfo("Naive Bayes Classifier", "The file 'train.csv' is missing")

        if(test == False):
            tkMessageBox.showinfo("Naive Bayes Classifier", "The file 'test.csv' is missing")

        if(bins == False):
            tkMessageBox.showinfo("Naive Bayes Classifier", "You have to enter a number for the Discretization bins")

        if(test == True & train == True & structure == True & bins == True):
            self.build()


root = Tk()
my_gui = Calculator(root)
root.mainloop()
