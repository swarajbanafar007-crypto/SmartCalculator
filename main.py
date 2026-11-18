import tkinter as tk
from tkinter import messagebox
from calculator import Calculator


class SmartCalculator:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Calculator")
        self.root.geometry("360x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#20232b")

        self.calculator = Calculator()
        self.expression = ""
        self.history = []

        title = tk.Label(
            root,
            text="SMART CALCULATOR",
            font=("Arial", 18, "bold"),
            bg="#20232b",
            fg="white"
        )
        title.pack(pady=15)

        self.display = tk.Entry(
            root,
            font=("Arial", 24),
            justify="right",
            bg="#303641",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=10
        )
        self.display.pack(
            fill="x", padx=15, pady=15, ipady=12
        )

        buttons = [
            ["C", "DEL", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "(", ")"],
            ["HISTORY", "=", "", ""]
        ]

        button_frame = tk.Frame(root, bg="#20232b")
        button_frame.pack(
            expand=True, fill="both", padx=10
        )

        for row_index, row in enumerate(buttons):
            for col_index, value in enumerate(row):

                if value == "":
                    continue

                button_color = "#414957"

                if value == "=":
                    button_color = "#16a085"
                elif value == "C":
                    button_color = "#e74c3c"
                elif value in ["+", "-", "*", "/", "%"]:
                    button_color = "#34495e"
                elif value == "HISTORY":
                    button_color = "#596275"

                button = tk.Label(
                    button_frame,
                    text=value,
                    font=("Arial", 14, "bold"),
                    bg=button_color,
                    fg="white",
                    relief="flat",
                    cursor="hand2"
                )

                button.grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew",
                    padx=4,
                    pady=4
                )

                button.bind(
                    "<Button-1>",
                    lambda event, v=value: self.click(v)
                )

        for i in range(6):
            button_frame.rowconfigure(i, weight=1)

        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

    def click(self, value):

        if value == "C":
            self.expression = ""

        elif value == "DEL":
            self.expression = self.expression[:-1]

        elif value == "=":
            self.calculate()
            return

        elif value == "HISTORY":
            messagebox.showinfo(
                "Calculation History",
                "\n".join(self.history[-10:])
                or "No history available"
            )
            return

        else:
            self.expression += value

        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    def calculate(self):

        try:
            allowed = set(
                "0123456789+-*/.()% "
            )

            if not self.expression or not all(
                char in allowed for char in self.expression
            ):
                raise ValueError

            result = eval(
                self.expression,
                {"__builtins__": {}},
                {}
            )

            if not isinstance(result, (int, float)):
                raise ValueError

            old_expression = self.expression
            self.expression = str(result)

            self.history.append(
                f"{old_expression} = {result}"
            )

            self.update_display()

        except ZeroDivisionError:
            messagebox.showerror(
                "Error",
                "Cannot divide by zero!"
            )

        except (ValueError, SyntaxError, TypeError):
            messagebox.showerror(
                "Error",
                "Invalid mathematical expression!"
            )


root = tk.Tk()
app = SmartCalculator(root)
root.mainloop()
