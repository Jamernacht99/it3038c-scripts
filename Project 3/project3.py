import tkinter as tk
import json
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar

def display_home():
    welcome_label.config(text="Welcome to Finance Tracker!")
    hide_cards()

def clear_label():
    welcome_label.config(text="")
    hide_cards()

def select_option(option):
    if option == "Home":
        display_home()
    elif option == "Cards":
        clear_label()
        show_cards()
    elif option == "Savings":
        clear_label()
        print("Savings functionality to be added")
    else:
        clear_label()
        print(f"Selected: {option}")

def show_cards():
    card_info_frame.pack(side=tk.TOP)  # Position the frame 1 quarter from the top
    load_cards()

def hide_cards():
    card_info_frame.pack_forget()  # Hide the frame containing card information

def load_cards():
    try:
        with open("cards.json", "r") as file:
            card_info = json.load(file)
            display_cards(card_info)
    except FileNotFoundError:
        display_cards([])  # Display an empty table if no cards exist


def display_cards(card_info):
    for widget in card_info_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(card_info_frame, text="Credit Cards", font=("Arial", 14, "bold"))
    title_label.pack()

    card_tree = ttk.Treeview(card_info_frame, columns=("Name", "Balance", "Next Due Date"), show="headings")
    card_tree.heading("Name", text="Name")
    card_tree.heading("Balance", text="Balance")
    card_tree.heading("Next Due Date", text="Next Due Date")

    for card in card_info:
        next_due_date = get_next_due_date(card['due_date'])
        card_tree.insert("", "end", values=(card['name'], card['balance'], next_due_date))

    card_tree.pack(expand=True, fill=tk.BOTH)

    add_card_button = tk.Button(card_info_frame, text="Add Card", command=display_add_card_prompt)
    add_card_button.pack()


def get_next_due_date(due_date):
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    if current_date.day <= int(due_date):
        next_due_date = datetime(current_year, current_month, int(due_date))
    else:
        if current_month == 12:
            next_due_date = datetime(current_year + 1, 1, int(due_date))
        else:
            next_due_date = datetime(current_year, current_month + 1, int(due_date))

    suffix = {1: "st", 2: "nd", 3: "rd"}.get(next_due_date.day % 10 if next_due_date.day % 10 < 4 and next_due_date.day not in [11, 12, 13] else 0, "th")
    return next_due_date.strftime("%B %d") + suffix

def display_add_card_prompt():
    add_card_window = tk.Toplevel(root)

    name_label = tk.Label(add_card_window, text="Name:")
    name_label.pack(padx=10, pady=5)
    name_entry = tk.Entry(add_card_window)
    name_entry.pack(padx=10, pady=5)

    due_date_label = tk.Label(add_card_window, text="Due Date (DD):")
    due_date_label.pack(padx=10, pady=5)
    
    # Create a Calendar widget to select the due date
    cal = Calendar(add_card_window, selectmode="day", date_pattern="dd/MM/yyyy")
    cal.pack(padx=10, pady=5)

    def get_due_date():
        due_date = cal.get_date().split("/")[0]  # Extract only the day from the selected date
        add_card(name_entry.get(), due_date, add_card_window)

    add_button = tk.Button(add_card_window, text="Add Card", command=get_due_date)
    add_button.pack(padx=10, pady=10)


def add_card(name, due_date, window):
    if not is_valid_name(name):
        print("Invalid name. Please enter a valid name.")
        return

    if not is_valid_day(due_date):
        print("Invalid day. Please enter a valid two-digit day number.")
        return

    try:
        with open("cards.json", "r") as file:
            card_info = json.load(file)
    except FileNotFoundError:
        card_info = []

    card_info.append({"name": name, "balance": "$0.00", "due_date": due_date})
    save_cards(card_info)
    display_cards(card_info)

    window.destroy()  # Close the add card window after adding the card


def save_cards(card_info):
    with open("cards.json", "w") as file:
        json.dump(card_info, file, indent=4)

def is_valid_name(name):
    # Add your validation criteria here
    if len(name) < 3 or len(name) > 20:
        return False
    return True

def is_valid_day(day):
    return day.isdigit() and len(day) == 2

def create_menu():
    global root, card_info_frame
    root = tk.Tk()
    root.title("Finance Tracker")
    root.geometry("800x600")

    navbar_frame = tk.Frame(root, bg="black")
    navbar_frame.pack(fill=tk.X)

    home_button = tk.Button(navbar_frame, text="Home", bg="white", fg="black", padx=10, pady=5,
                            command=lambda: select_option("Home"))
    home_button.pack(side=tk.LEFT, padx=10, pady=10)

    cards_button = tk.Button(navbar_frame, text="Cards", bg="white", fg="black", padx=10, pady=5,
                             command=lambda: select_option("Cards"))
    cards_button.pack(side=tk.LEFT, padx=10, pady=10)

    savings_button = tk.Button(navbar_frame, text="Savings", bg="white", fg="black", padx=10, pady=5,
                               command=lambda: select_option("Savings"))
    savings_button.pack(side=tk.LEFT, padx=10, pady=10)

    global welcome_label
    welcome_label = tk.Label(root, text="", font=("Arial", 18))
    welcome_label.pack(pady=50)

    card_info_frame = tk.Frame(root)  # Frame for displaying card information

    display_home()

    root.mainloop()

if __name__ == "__main__":
    create_menu()
