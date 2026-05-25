import tkinter as tk
import math
import ast


# Function to clear input

def clear():
    entry.delete(0, tk.END)
    result_label.config(text="Result:")


# Main window

root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("400x300")
root.resizable(False, False)


# Title

title = tk.Label(root, text="Scientific Calculator", font=("Arial", 18))
title.pack(pady=10)

def calculate():
    try:
        expression = entry.get()

        result = eval(expression, {
            "__builtins__": None,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log": math.log,
            "pi": math.pi,
            "e": math.e
        })

        result_label.config(text=f"Result: {result}")

    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Input box

entry = tk.Entry(root, font=("Arial", 16), width=25)
entry.pack(pady=10)


# Buttons frame

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


# Calculate button

calculate_button = tk.Button(
    button_frame,
    text="Calculate",
    font=("Arial", 12),
    command=calculate,
    width=12
)

calculate_button.grid(row=0, column=0, padx=10)


# Clear button

clear_button = tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 12),
    command=clear,
    width=12
)

clear_button.grid(row=0, column=1, padx=10)


# Result label

result_label = tk.Label(root, text="Result:", font=("Arial", 14))
result_label.pack(pady=20)


# Help text

help_text = tk.Label(
    root,
    text="Examples: sin(pi/2), sqrt(25), log10(100)",
    font=("Arial", 10)
)

help_text.pack()


# Run app

root.mainloop()