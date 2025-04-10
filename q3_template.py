# -*- coding: utf-8 -*-

# Enter your candidate ID here:
# Enter your student ID here:
# Do NOT enter your name

# 4QQMN506 Coursework Q3

import breezypythongui as bpg  
from datetime import datetime

class AgeCalculator(bpg.EasyFrame):
    """Application that calculates how long a person has been alive."""
    
    def __init__(self):
        """Sets up the window and widgets."""
        bpg.EasyFrame.__init__(self, title="Age Calculator", width=400, height=600)
        self.addLabel("Enter Your Birthdate", 0, 0, columnspan=2)
        # Add input fields for birth date
        self.addLabel("Year (Enter Integer):", 1, 0)
        self.birthYear = self.addIntegerField(0, 1, 1)
        
        self.addLabel("Month (Enter Integer between 1-12):", 2, 0)
        self.birthMonth = self.addIntegerField(0, 2, 1)
        
        self.addLabel("Day (Enter Integer between 1-31):", 3, 0)
        self.birthDay = self.addIntegerField(0, 3, 1)
        
        # Add input fields for birth time
        self.addLabel("Enter Your Birth Time", 4, 0)
        self.addLabel("Hour (Enter Integer between 0-23):", 5, 0)
        self.birthHour = self.addIntegerField(0, 5, 1)
        
        self.addLabel("Minute:(Enter Integer between 0-59)", 6, 0)
        self.birthMinute = self.addIntegerField(0, 6, 1)
        
        # Add buttons side by side
        self.addButton("Calculate", 7, 0, command=self.calculate)
        self.addButton("Clear", 8, 0, command=self.clear)
        
        # Add text area for displaying results
        self.outputArea = self.addTextArea("", 9, 0, columnspan=2, width=50, height=5)
    
    def calculate(self):
        """Calculates and displays how long the person has been alive."""
        try:
            # Check if any input fields are empty
            if (self.birthYear.getValue() == 0 or 
                self.birthMonth.getValue() == 0 or
                self.birthDay.getValue() == 0 ):
                
                # Display an error message box
                self.messageBox(title="Input Error", 
                               message="Please fill in all fields before calculating.",
                               width=30)
                return
            
            # Get input values
            year = self.birthYear.getNumber()
            month = self.birthMonth.getNumber()
            day = self.birthDay.getNumber()
            hour = self.birthHour.getNumber()
            minute = self.birthMinute.getNumber()
            
            # Validate input boundaries
            error_message = ""
            if month < 1 or month > 12:
                error_message += "Month must be between 1 and 12.\n"
            if day < 1 or day > 31:
                error_message += "Day must be between 1 and 31.\n"
            if hour < 0 or hour > 23:
                error_message += "Hour must be between 0 and 23.\n"
            if minute < 0 or minute > 59:
                error_message += "Minute must be between 0 and 59.\n"
            
            # If any validation errors, display message box and return
            if error_message:
                self.messageBox(title="Invalid Input", 
                               message=error_message,
                               width=30)
                return
            
            # Check if birth date is in the future
            try:
                # Create datetime object for birth date/time
                birth_datetime = datetime(year, month, day, hour, minute)
                
                # Get current datetime
                current_datetime = datetime.now()
                
                # Check if birth date is in the future
                if birth_datetime > current_datetime:
                    self.messageBox(title="Invalid Date", 
                                   message="Birth date cannot be in the future.",
                                   width=30)
                    return
                    
                # Calculate the time difference
                time_diff = current_datetime - birth_datetime
                
                # Get total duration in seconds
                total_seconds = time_diff.total_seconds()
                
                # Calculate different time units with 2 decimal places
                years = round(total_seconds / (365.25 * 24 * 60 * 60), 2)
                days = round(total_seconds / (24 * 60 * 60), 2)
                hours = round(total_seconds / (60 * 60), 2)
                minutes = round(total_seconds / 60, 2)
                seconds = round(total_seconds, 2)
                
                # Format the output message
                result_message = f"You have been alive for:\n"
                result_message += f"{years} years,\n"
                result_message += f"{days} days,\n"
                result_message += f"{hours} hours,\n"
                result_message += f"{minutes} minutes,\n"
                result_message += f"{seconds} seconds"
                
                self.outputArea.setText(result_message)
            
            except ValueError as e:
                # Handle invalid date combinations (like February 30)
                self.messageBox(title="Invalid Date", 
                               message="Invalid date combination. Please check your inputs.",
                               width=30)
                
        except Exception as e:
            self.outputArea.setText(f"Error: {str(e)}\nPlease check your inputs.")
    
    def clear(self):
        """Clears all input fields and the output area."""
        self.birthYear.setNumber(0)
        self.birthMonth.setNumber(0)
        self.birthDay.setNumber(0)
        self.birthHour.setNumber(0)
        self.birthMinute.setNumber(0)
        self.outputArea.setText("")

def main():
    """Instantiate and pop up the window."""
    AgeCalculator().mainloop()

if __name__ == "__main__":
    main()