import tkinter as tk
from tkinter import Canvas
import csv
import os


class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.root.title("Perfect Histogram")
        self.canvas_width = 900
        self.canvas_height = 600
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="lightgray")
        self.canvas.pack()
        self.max_frequency = max(max(val1, val2) for val1, val2 in traffic_data) or 1  # Avoid zero division

    def setup_window(self):
        """
        Sets up the canvas for the histogram.
        """
        self.canvas.create_text(self.canvas_width // 2, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
                                font=("Arial", 16, "bold"))
        self.canvas.create_rectangle(100, 50, 850, 550, outline="black")  # Draw main histogram area
        self.canvas.create_text(self.canvas_width // 2, 580, text="Hours (00:00 to 23:00)", font=("Arial", 10, "italic"))

    def draw_axes(self):
        """
        Draws axes with labels and grid lines.
        """
        # X-axis (hours)
        for i in range(24):
            x = 100 + i * 31
            self.canvas.create_text(x + 15, 560, text=f"{i:02}", font=("Arial", 9))
            self.canvas.create_line(x + 15, 550, x + 15, 545, fill="black")  # Minor tick marks

        # Y-axis (frequencies)
        for i in range(0, self.max_frequency + 1, max(1, self.max_frequency // 10)):
            y = 550 - (i * 500 // self.max_frequency)  # Scale frequencies to fit
            self.canvas.create_text(90, y, text=f"{i}", font=("Arial", 9), anchor="e")
            self.canvas.create_line(100, y, 850, y, fill="gray", dash=(2, 2))  # Grid lines for better visualization

    def draw_histogram(self):
        """
        Draws the bars for the histogram.
        """
        bar_gap = 31  # Distance between bar groups
        bar_width = 10  # Width of each bar
        for hour, (val1, val2) in enumerate(self.traffic_data):
            x_center = 100 + hour * bar_gap + 15  # Center of the hour slot
            y1 = 550 - (val1 * 500 // self.max_frequency)  # Scale bar height
            y2 = 550 - (val2 * 500 // self.max_frequency)

            # Bar for Elm Avenue/Rabbit Road (green)
            self.canvas.create_rectangle(x_center - bar_width - 2, y1, x_center - 2, 550, fill="green", outline="black")
            if val1 > 0:
                self.canvas.create_text(x_center - bar_width, y1 - 10, text=str(val1), font=("Arial", 8), fill="black")

            # Bar for Hanley Highway/Westway (red)
            self.canvas.create_rectangle(x_center + 2, y2, x_center + bar_width + 2, 550, fill="red", outline="black")
            if val2 > 0:
                self.canvas.create_text(x_center + bar_width, y2 - 10, text=str(val2), font=("Arial", 8), fill="black")

    def add_legend(self):
        """
        Adds a legend to the histogram.
        """
        self.canvas.create_rectangle(700, 80, 850, 130, fill="white", outline="black")
        self.canvas.create_rectangle(710, 90, 730, 110, fill="green", outline="black")
        self.canvas.create_text(740, 100, text="Elm Avenue/Rabbit Road", font=("Arial", 10), anchor="w")

        self.canvas.create_rectangle(710, 110, 730, 130, fill="red", outline="black")
        self.canvas.create_text(740, 120, text="Hanley Highway/Westway", font=("Arial", 10), anchor="w")

    def run(self):
        """
        Runs the application.
        """
        self.setup_window()
        self.draw_axes()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()


class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    @staticmethod
    def validate_date_input(date_input, value_type):
        """
        Validates the date input based on the type (day, month, or year).
        """
        try:
            value = int(date_input)
            if value_type == "day" and (1 <= value <= 31):
                return value
            elif value_type == "month" and (1 <= value <= 12):
                return value
            elif value_type == "year" and (2000 <= value <= 2024):
                return value
            else:
                raise ValueError
        except ValueError:
            print(f"Out of range - value must be valid for {value_type}.")
            return None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")
        data = []
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    hour = int(row['timeOfDay'].split(':')[0])
                    if len(data) <= hour:
                        data.extend([[0, 0]] * (hour + 1 - len(data)))
                    if row['JunctionName'] == 'Elm Avenue/Rabbit Road':
                        data[hour][0] += 1
                    elif row['JunctionName'] == 'Hanley Highway/Westway':
                        data[hour][1] += 1
            return data
        except Exception as e:
            raise RuntimeError(f"Error reading CSV file: {e}")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:
            # Collect date inputs
            while True:
                day = self.validate_date_input(input("Enter the day (DD): "), "day")
                if day is not None:
                    break

            while True:
                month = self.validate_date_input(input("Enter the month (MM): "), "month")
                if month is not None:
                    break

            while True:
                year = self.validate_date_input(input("Enter the year (YYYY): "), "year")
                if year is not None:
                    break

            date = f"{day:02}{month:02}{year}"
            file_path = f"traffic_data{date}.csv"

            try:
                self.current_data = self.load_csv_file(file_path)
                print(f"Successfully loaded data from {file_path}.")
                app = HistogramApp(self.current_data, f"{day:02}/{month:02}/{year}")
                app.run()
            except Exception as e:
                print(f"Error: {e}")

            # Loop control
            while True:
                choice = input("Do you want to select another dataset (Y/N)? ").strip().lower()
                if choice in ['y', 'n']:
                    break
                print("Invalid input. Please enter 'Y' or 'N'.")

            if choice == 'n':
                print("Exiting the program.")
                break


def main():
    """
    Entry point for the program.
    """
    print("Welcome to the Traffic Data Analysis Program!")
    processor = MultiCSVProcessor()
    processor.process_files()


if __name__ == "__main__":
    main()
