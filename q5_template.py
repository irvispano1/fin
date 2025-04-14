# -*- coding: utf-8 -*-


# Enter your candidate ID here:
# Enter your student ID here:
# Do NOT enter your name

# 4QQMN506 Coursework Q5

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from breezypythongui import EasyFrame
from tkinter import messagebox
import tkinter as tk
import os
import numpy as np
import re
from tkinter.filedialog import askopenfilename

class FinancialDataApp(EasyFrame):
    """Stock Plotter"""

    def __init__(self):
        
        EasyFrame.__init__(self, title="Stock Plotter", width=1000, height=700)
        
        
        self.df = None
        self.fig = None
        self.canvas = None
        self.ax = None
        self.canvas_widget = None
        
       
        self.setupUI()
    
    def setupUI(self): 
        self.addButton("Enter CSV File", 1, 0, command=self.load_csv)        
        
        self.addLabel("Select RIC:", 2, 0)
        self.ricCombo = self.addCombobox("", ["Select a RIC..."], 2, 1)
        
        
        self.addLabel("Start Date (dd/mm/yyyy):", 3, 0)
        self.startDateField = self.addTextField("", 3, 1)
        
        
        self.addLabel("End Date (dd/mm/yyyy):", 4, 0)
        self.endDateField = self.addTextField("", 4, 1)
        
        
        self.addButton("Plot", 5, 1, command=self.plot_data)
        self.addButton("Clear All", 5, 2, command=self.clear_all)
        self.plotPanel = self.addPanel(7, 0, rowspan=4, columnspan=2, background="white")
        self.addButton("Calculate Return", 10, 1, command=self.calculate_return)
        self.addButton("Calculate Std Dev", 10, 2, command=self.calculate_std_dev)
        
        
        self.addButton("Clear Plot", 6, 1, command=self.clear_plot)
        
        
        
    def load_csv(self):        
        try:            
            file_path = askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            
           
            if not file_path:
                return
                
            self.df = pd.read_csv(file_path)           

            self.df['Date'] = pd.to_datetime(self.df['Dates'], format='%d/%m/%Y')
            
            
            self.df.set_index('Date', inplace=True)
            
            
            ric_codes = list(self.df.columns)
            
            # Update the RIC 
            self.ricCombo["values"] = ric_codes
            
            messagebox.showinfo("Success", "CSV file loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file Not Found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error with CSV file: {str(e)}")
    
    def validate_input(self):
        
        if self.df is None:
            messagebox.showerror("Error", "Please load a CSV file first.")
            return None
        
        
        selected_ric = self.ricCombo.getText()
        if not selected_ric:
            messagebox.showerror("Error", "Please fill in all fields.")
            return None
        
        
        start_date_str = self.startDateField.getText().strip()
        end_date_str = self.endDateField.getText().strip()
        
        if not start_date_str or not end_date_str:
            messagebox.showerror("Error", "Please fill in all fields.")
            return None
        
        
        date_pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
        if not re.match(date_pattern, start_date_str) or not re.match(date_pattern, end_date_str):
            messagebox.showerror("Error", "Incorrect date format. Please use dd/mm/yyyy.")
            return None
        
        try:
            
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
            
            
            if start_date >= end_date:
                if start_date == end_date:
                    messagebox.showerror("Error", "Start date and end date cannot be the same.")
                else:
                    messagebox.showerror("Error", "Start date must be earlier date than end date.")
                return None
            
            
            min_date = self.df.index.min()
            max_date = self.df.index.max()
            
            if start_date < min_date:
                messagebox.showerror("Error", f"Start date cannot be less than the earliest date in data ({min_date.strftime('%d/%m/%Y')})")
                return None
                
            if end_date > max_date:
                messagebox.showerror("Error", f"End date cannot be greater than the latest date in data ({max_date.strftime('%d/%m/%Y')})")
                return None
                
            return selected_ric, start_date, end_date
            
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use dd/mm/yyyy.")
            return None
            
    def plot_data(self):
        
        validation_result = self.validate_input()
        if validation_result is None:
            return
            
        selected_ric, start_date, end_date = validation_result
        
        
        filtered_data = self.df.loc[start_date:end_date, selected_ric]
        
        
        self.clear_plot()
        
        
        self.fig = Figure(figsize=(7, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        
        self.ax.plot(filtered_data.index, filtered_data, 'b-')
        self.ax.set_title(f"{selected_ric} Stock Price")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Price")
        self.ax.grid(True)
        
        
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
        
        
        self.fig.tight_layout()
        
        
        if self.canvas_widget is None:
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotPanel)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        else:
            
            self.canvas.figure = self.fig
        
        
        self.canvas.draw()
    
    def calculate_return(self):
        
        validation_result = self.validate_input()
        if validation_result is None:
            return
            
        selected_ric, start_date, end_date = validation_result
        
        
        filtered_data = self.df.loc[start_date:end_date, selected_ric]
        
        
        start_price = filtered_data.iloc[0]
        end_price = filtered_data.iloc[-1]
        return_value = ((end_price - start_price) / start_price) * 100
        
        
        messagebox.showinfo("Simple Percentage Return", 
                           f"Simple Percentage Return from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}: {return_value:.2f}%")
    
    def calculate_std_dev(self):
        
        validation_result = self.validate_input()
        if validation_result is None:
            return
            
        selected_ric, start_date, end_date = validation_result
        
        
        filtered_data = self.df.loc[start_date:end_date, selected_ric]
        
        
        std_dev = np.std(filtered_data)
        
        
        messagebox.showinfo("Standard Deviation", 
                           f"Standard Deviation for {selected_ric} prices from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}: {std_dev:.4f}")
    
    def clear_all(self):
        
        self.startDateField.setText("")
        self.endDateField.setText("")
        self.ricCombo.setText("")
        self.clear_plot()
    
    def clear_plot(self):
        
        if self.canvas_widget is not None:
            self.canvas_widget.pack_forget()
            self.canvas_widget = None
            self.fig = None
            self.ax = None
            self.canvas = None

def main():
    
    FinancialDataApp().mainloop()

if __name__ == "__main__":
    main()







#  Comments on the code below are not related to the above code 
# 5.6
# A GUI application is more user friendly, and users interact easily, 
# while in terminal-based interface would require users to remember different kind of commands
# and reference a documentation. This app requires vizualizing plots of stocks 
# and statistical ones and doing this with a terminal is not suitable, instead for a GUI application 
# can display and implement visual elements like charts and plots. 
# GUIs are easier for error handling communicating errors and easier for uploading files 
# and working with data compared to terminal based applications which would require rememberin 
# and using complicated commands. You can learn and work faster with GUI apps. 
# You can do things simultaneously instead of writing a separate command on terminal.

# 5.7
# 5.8What are instance variables, and what role does the name self play in the context of a class definition?
# A class when is initiated by the init method creates an instance of itself 
# and is called an object. 
# The object contains certain variables and methods and is referenced as self.
# and object uses its class as a blueprint but can contain different values of its instance variables 
# example class Person creates an personobject= self.hair_color  is related to that specific person
# 5.9
# 5.10