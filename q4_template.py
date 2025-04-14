# -*- coding: utf-8 -*-

import breezypythongui as bpg
from tkinter.filedialog import askopenfilename, asksaveasfilename

class TextEditor(bpg.EasyFrame):
   

    def __init__(self):
        
        bpg.EasyFrame.__init__(self, title="Text Editor", width=700, height=700)
        self.addLabel("Text Editor", 0, 0, columnspan=2)

        self.textArea = self.addTextArea("", 1, 0, columnspan=2, width=60, height=20)

        self.addButton("Open", 2, 1, command=self.openFile)
        self.addButton("Save", 2, 2, command=self.saveFile)
        self.addButton("New", 2, 0, command=self.newFile)

    def openFile(self):        
        filePath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filePath:
            with open(filePath, "r") as file:
                content = file.read()
            self.textArea.setText(content)

    def saveFile(self):        
        filePath = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filePath:
            with open(filePath, "w") as file:
                file.write(self.textArea.getText())

    def newFile(self):        
        self.textArea.setText("")

def main():    
    TextEditor().mainloop()

if __name__ == "__main__":
    main()