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
    """A GUI application for financial data analysis."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title="Financial Data Analysis", width=900, height=700)
        
        # Initialize variables
        self.df = None
        self.fig = None
        self.canvas = None
        self.ax = None
        self.canvas_widget = None
        
        # Set up the UI layout
        self.setupUI()
    
    def setupUI(self):
        """Sets up all the UI components."""
        # Row 0: CSV file loading
        self.addLabel("Financial Data Analysis", 0, 0, columnspan=3, 
                     font=("Arial", 16, "bold"), background="lightgray")
        
        # Row 1: Load CSV button
        self.addButton("Load CSV", 1, 0, command=self.loadCSV)
        
        # Row 2: RIC Selection
        self.addLabel("Select RIC:", 2, 0, sticky="E")
        self.ricCombo = self.addCombobox("", ["Select a RIC..."], 2, 1)
        
        # Row 3: Start Date
        self.addLabel("Start Date (dd/mm/yyyy):", 3, 0, sticky="E")
        self.startDateField = self.addTextField("", 3, 1)
        
        # Row 4: End Date
        self.addLabel("End Date (dd/mm/yyyy):", 4, 0, sticky="E")
        self.endDateField = self.addTextField("", 4, 1)
        
        # Row 5: Action buttons
        self.addButton("Plot", 5, 0, command=self.plotData)
        self.addButton("Calculate Return", 5, 1, command=self.calculateReturn)
        self.addButton("Calculate Std Dev", 5, 2, command=self.calculateStdDev)
        
        # Row 6: Clear buttons
        self.addButton("Clear All", 6, 0, command=self.clearAll)
        self.addButton("Clear Plot", 6, 1, command=self.clearPlot)
        
        # Row 7-12: Plot area
        self.plotPanel = self.addPanel(7, 0, rowspan=5, columnspan=3, background="white")
        
    def loadCSV(self):
        """Loads a CSV file selected by the user and populates the RIC dropdown."""
        try:
            # Open file dialog for the user to select a CSV file
            file_path = askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            
            # If user cancels the dialog, file_path will be empty
            if not file_path:
                return
                
            self.df = pd.read_csv(file_path)
            
            # Convert the date column to datetime format
            self.df['Date'] = pd.to_datetime(self.df['Dates'], format='%d/%m/%Y')
            
            # Set the date as index
            self.df.set_index('Date', inplace=True)
            
            # Get RIC codes (column headers excluding Date)
            ric_codes = list(self.df.columns)
            
            # Update the RIC combobox
            self.ricCombo["values"] = ric_codes
            
            messagebox.showinfo("Success", "CSV file loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading CSV file: {str(e)}")
    
    def validateInputs(self):
        """Validates user inputs and returns processed dates if valid."""
        if self.df is None:
            messagebox.showerror("Error", "Please load a CSV file first.")
            return None
        
        # Get selected RIC
        selected_ric = self.ricCombo.getText()
        if not selected_ric:
            messagebox.showerror("Error", "Please fill in all fields.")
            return None
        
        # Get and validate dates
        start_date_str = self.startDateField.getText().strip()
        end_date_str = self.endDateField.getText().strip()
        
        if not start_date_str or not end_date_str:
            messagebox.showerror("Error", "Please fill in all fields.")
            return None
        
        # Check date format using regex
        date_pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
        if not re.match(date_pattern, start_date_str) or not re.match(date_pattern, end_date_str):
            messagebox.showerror("Error", "Incorrect date format. Please use dd/mm/yyyy.")
            return None
        
        try:
            # Convert to datetime objects
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
            
            # Check if start date is after end date
            if start_date >= end_date:
                if start_date == end_date:
                    messagebox.showerror("Error", "Start date cannot be equal to end date.")
                else:
                    messagebox.showerror("Error", "Start date cannot be after end date.")
                return None
            
            # Check if dates are within range of data
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
            
    def plotData(self):
        """Plots the selected RIC data between the specified dates."""
        validation_result = self.validateInputs()
        if validation_result is None:
            return
            
        selected_ric, start_date, end_date = validation_result
        
        # Filter data based on date range
        filtered_data = self.df.loc[start_date:end_date, selected_ric]
        
        # Clear existing plot if any
        self.clearPlot()
        
        # Create a new figure and canvas
        self.fig = Figure(figsize=(7, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Plot the data
        self.ax.plot(filtered_data.index, filtered_data, 'b-')
        self.ax.set_title(f"{selected_ric} Stock Price")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Price")
        self.ax.grid(True)
        
        # Rotate date labels for better readability
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
        
        # Adjust layout
        self.fig.tight_layout()
        
        # Create canvas widget if it doesn't exist
        if self.canvas_widget is None:
            # Create a canvas for the plot
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotPanel)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        else:
            # Update the existing canvas
            self.canvas.figure = self.fig
        
        # Draw the plot
        self.canvas.draw()
    
    def calculateReturn(self):
        """Calculates and displays the return for the selected date range."""
        validation_result = self.validateInputs()
        if validation_result is None:
            return
            
        selected_ric, start_date, end_date = validation_result
        
        # Filter data based on date range
        filtered_data = self.df.loc[start_date:end_date, selected_ric]
        
        # Calculate return as percentage
        start_price = filtered_data.iloc[0]
        end_price = filtered_data.iloc[-1]
        return_value = ((end_price - start_price) / start_price) * 100
        
        # Display result
        messagebox.showinfo("Return Calculation", 
                           f"Return for {selected_ric} from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}: {return_value:.2f}%")
    
    def calculateStdDev(self):
        """Calculates and displays the standard deviation for the selected date range."""
        validation_result = self.validateInputs()
        if validation_result is None:
            return
            
        selected_ric, start_date, end_date = validation_result
        
        # Filter data based on date range
        filtered_data = self.df.loc[start_date:end_date, selected_ric]
        
        # Calculate standard deviation
        std_dev = np.std(filtered_data)
        
        # Display result
        messagebox.showinfo("Standard Deviation", 
                           f"Standard Deviation for {selected_ric} from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}: {std_dev:.4f}")
    
    def clearAll(self):
        """Clears all inputs and resets the dropdown."""
        self.startDateField.setText("")
        self.endDateField.setText("")
        self.ricCombo.setText("")
        self.clearPlot()
    
    def clearPlot(self):
        """Clears the plot area."""
        if self.canvas_widget is not None:
            self.canvas_widget.pack_forget()
            self.canvas_widget = None
            self.fig = None
            self.ax = None
            self.canvas = None

def main():
    """Runs the financial data application."""
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