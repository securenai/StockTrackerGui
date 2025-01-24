import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Stock Tracker App")
        self.geometry("500x400")

        # Dictionary to hold frames (pages)
        self.frames = {}

        # Create pages
        for Page in (MainPage, SettingsPage):
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start with the main page
        self.show_frame("MainPage")

    def show_frame(self, page_name):
        """Show a specific frame by its name."""
        frame = self.frames[page_name]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # UI for the Main Page
        label = tk.Label(self, text="Welcome to the Stock Tracker App", font=("Arial", 16))
        label.pack(pady=20)

        # Button to navigate to Settings Page
        settings_button = tk.Button(self, text="Go to Settings", command=lambda: controller.show_frame("SettingsPage"))
        settings_button.pack()


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Return button to go back to Main Page (placed at the top)
        return_button = tk.Button(self, text="Return to Main Page", command=lambda: controller.show_frame("MainPage"))
        return_button.pack(pady=10)

        # Title for the Settings Page
        label = tk.Label(self, text="Settings - Manage Stock Symbols", font=("Arial", 16))
        label.pack(pady=10)

        # Input field for adding stock symbols
        tk.Label(self, text="Add a Stock Symbol:", font=("Arial", 12)).pack()
        self.stock_entry = ttk.Entry(self, width=30)
        self.stock_entry.pack(pady=10)

        # Save button
        save_button = tk.Button(self, text="Save Stock Symbol", command=self.save_stock_symbol)
        save_button.pack(pady=10)

        # Input field for removing stock symbols
        tk.Label(self, text="Remove a Stock Symbol:", font=("Arial", 12)).pack()
        self.remove_entry = ttk.Entry(self, width=30)
        self.remove_entry.pack(pady=10)

        # Remove button
        remove_button = tk.Button(self, text="Remove Stock Symbol", command=self.remove_stock_symbol)
        remove_button.pack(pady=10)

        # Section to display saved stocks
        self.saved_stocks_label = tk.Label(self, text="Saved Stock Symbols:", font=("Arial", 12))
        self.saved_stocks_label.pack(pady=10)

        self.stocks_list = tk.Text(self, width=40, height=10, state="disabled")
        self.stocks_list.pack(pady=10)

        # Load and display saved stocks initially
        self.display_saved_stocks()

    def save_stock_symbol(self):
        """Save the entered stock symbol to a file."""
        stock_symbol = self.stock_entry.get().strip()
        if stock_symbol:
            try:
                # Append to file
                with open("stocks.txt", "a") as f:
                    f.write(stock_symbol + "\n")
                self.stock_entry.delete(0, tk.END)  # Clear input field
                self.display_saved_stocks()  # Update the displayed stock symbols
            except Exception as e:
                print(f"Error saving stock: {e}")

    def remove_stock_symbol(self):
        """Remove a specific stock symbol from the file."""
        stock_symbol = self.remove_entry.get().strip()
        if not stock_symbol:
            return  # Do nothing if the input is empty

        try:
            # Read all stock symbols from the file
            with open("stocks.txt", "r") as f:
                stocks = f.readlines()

            # Rewrite the file without the selected stock symbol
            with open("stocks.txt", "w") as f:
                for stock in stocks:
                    if stock.strip().lower() != stock_symbol.lower():
                        f.write(stock)

            self.remove_entry.delete(0, tk.END)  # Clear the input field
            self.display_saved_stocks()  # Refresh the displayed list
        except FileNotFoundError:
            print("No stocks file found.")
        except Exception as e:
            print(f"Error removing stock: {e}")

    def display_saved_stocks(self):
        """Load and display stock symbols from the file."""
        try:
            with open("stocks.txt", "r") as f:
                saved_stocks = f.readlines()
        except FileNotFoundError:
            saved_stocks = []

        self.stocks_list.config(state="normal")
        self.stocks_list.delete("1.0", tk.END)  # Clear previous content
        for stock in saved_stocks:
            self.stocks_list.insert(tk.END, stock.strip() + "\n")
        self.stocks_list.config(state="disabled")


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
