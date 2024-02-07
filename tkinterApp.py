import tkinter as tk
from tkinter import messagebox

# Encapsulation: The Calculator class encapsulates the functionality related to the GUI elements and calculations.
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Calculator")

        # Encapsulation: The input_label, input_entry, square_button, and cube_button are encapsulated within the Calculator class.
        self.input_label = tk.Label(root, text="Enter a number:")
        self.input_label.pack()

        self.input_entry = tk.Entry(root)
        self.input_entry.pack()

        self.square_button = tk.Button(root, text="Calculate Square", command=self.calculate_square)
        self.square_button.pack()

        self.cube_button = tk.Button(root, text="Calculate Cube", command=self.calculate_cube)
        self.cube_button.pack()

    # Decorators: The validate_input decorator is used to validate user input before executing the calculate_square and calculate_cube methods.
    def validate_input(func):
        def wrapper(self):
            try:
                number = int(self.input_entry.get())
                if number < 0:
                    raise ValueError("Number must be positive")
                return func(self)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        return wrapper

    # Method Overriding: The calculate_square method overrides the validate_input decorator to validate input specifically for calculating the square.
    @validate_input
    def calculate_square(self):
        number = int(self.input_entry.get())
        result = number ** 2
        messagebox.showinfo("Result", f"The square of {number} is {result}")

    # Method Overriding: The calculate_cube method overrides the validate_input decorator to validate input specifically for calculating the cube.
    @validate_input
    def calculate_cube(self):
        number = int(self.input_entry.get())
        result = number ** 3
        messagebox.showinfo("Result", f"The cube of {number} is {result}")

root = tk.Tk()
calculator = Calculator(root)
root.mainloop()
