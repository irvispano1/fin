# -*- coding: utf-8 -*-

import breezypythongui as bpg
from tkinter.filedialog import askopenfilename, asksaveasfilename

class TextEditor(bpg.EasyFrame):
    """A simple text editor application."""

    def __init__(self):
        """Sets up the window and widgets."""
        bpg.EasyFrame.__init__(self, title="Text Editor", width=700, height=700)

        # Add a label for the text area
        self.addLabel("Text Editor", 0, 0, columnspan=2)

        # Add a multiline text area with a vertical scrollbar
        self.textArea = self.addTextArea("", 1, 0, columnspan=2, width=60, height=20)

        # Add buttons for Open, Save, and New
        self.addButton("Open", 2, 1, command=self.openFile)
        self.addButton("Save", 2, 2, command=self.saveFile)
        self.addButton("New", 2, 0, command=self.newFile)

    def openFile(self):
        """Opens a file and loads its content into the text area."""
        filePath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filePath:
            with open(filePath, "r") as file:
                content = file.read()
            self.textArea.setText(content)

    def saveFile(self):
        """Saves the content of the text area to a file."""
        filePath = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filePath:
            with open(filePath, "w") as file:
                file.write(self.textArea.getText())

    def newFile(self):
        """Clears the text area to create a new file."""
        self.textArea.setText("")

def main():
    """Runs the text editor application."""
    TextEditor().mainloop()

if __name__ == "__main__":
    main()