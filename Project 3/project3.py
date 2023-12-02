import tkinter as tk
import json
from tkinter import ttk
from datetime import datetime
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
    elif option == "Checking":
        clear_label()
        print("Checking functionality to be added")
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

def display_activity_detail(card_name):
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Activities for {card_name}")

    activities = load_activities(card_name)

    activity_tree = ttk.Treeview(detail_window, columns=("Date", "Amount", "Type", "Description"), show="headings")
    activity_tree.heading("Date", text="Date")
    activity_tree.heading("Amount", text="Amount")
    activity_tree.heading("Type", text="Type")
    activity_tree.heading("Description", text="Description")

    for activity in activities:
        activity_tree.insert("", "end", values=(activity['date'], activity['amount'], activity['type'], activity['description']))

    activity_tree.pack(expand=True, fill=tk.BOTH)

    add_activity_button = tk.Button(detail_window, text="Add Activity", command=lambda: display_add_activity_prompt(card_name))
    add_activity_button.pack()

def load_activities(card_name):
    try:
        with open(f"{card_name}_activities.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_activities(card_name, activities):
    with open(f"{card_name}_activities.json", "w") as file:
        json.dump(activities, file, indent=4)

def on_select_card(event):
    selected_item = card_tree.focus()
    card_name = card_tree.item(selected_item)['values'][0]

    display_activity_detail(card_name)

def display_cards(card_info):
    for widget in card_info_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(card_info_frame, text="Credit Cards", font=("Arial", 14, "bold"))
    title_label.pack()

    global card_tree
    card_tree = ttk.Treeview(card_info_frame, columns=("Name", "Balance", "Next Due Date"), show="headings")
    card_tree.heading("Name", text="Name")
    card_tree.heading("Balance", text="Balance")
    card_tree.heading("Next Due Date", text="Next Due Date")

    for card in card_info:
        next_due_date = get_next_due_date(card['due_date'])
        card_tree.insert("", "end", values=(card['name'], card['balance'], next_due_date))

    card_tree.bind("<Double-1>", on_select_card)  # Bind double-click event to the card_tree

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

def display_add_activity_prompt(card_name):
    add_activity_window = tk.Toplevel(root)
    add_activity_window.title(f"Add Activity for {card_name}")

    date_label = tk.Label(add_activity_window, text="Date:")
    date_label.pack(padx=10, pady=5)
    # Create a Calendar widget to select the date
    cal = Calendar(add_activity_window, selectmode="day", date_pattern="dd/MM/yyyy")
    cal.pack(padx=10, pady=5)

    def validate_amount_input(value):
        if value == "":
            return True
        try:
            if '.' not in value:
                float(value + '.00')
                return True
            # Otherwise, validate the input as usual
            else:
                float(value)
                if value.count(".") <= 1:
                    if len(value.split(".")[-1]) <= 2:
                        return True
        except ValueError:
            return False
        return False

    amount_label = tk.Label(add_activity_window, text="Amount:")
    amount_label.pack(padx=10, pady=5)
    amount_var = tk.StringVar()
    validate_amount = (add_activity_window.register(validate_amount_input), "%P")
    amount_entry = tk.Entry(add_activity_window, textvariable=amount_var, validate="key", validatecommand=validate_amount)
    amount_entry.pack(padx=10, pady=5)

    type_label = tk.Label(add_activity_window, text="Type:")
    type_label.pack(padx=10, pady=5)
    type_var = tk.StringVar(add_activity_window)
    type_var.set("Credit")  # Default value
    type_dropdown = tk.OptionMenu(add_activity_window, type_var, "Credit", "Debit")
    type_dropdown.pack(padx=10, pady=5)

    description_label = tk.Label(add_activity_window, text="Description:")
    description_label.pack(padx=10, pady=5)
    description_entry = tk.Entry(add_activity_window)
    description_entry.pack(padx=10, pady=5)

    def add_activity():
        entered_amount = amount_entry.get()
        if '.' not in entered_amount:
            entered_amount += '.00'  # Append ".00" if no decimal is present

        activity_data = {
            "date": cal.get_date(),
            "amount": entered_amount,
        "type": type_var.get(),
        "description": description_entry.get()
    }

        save_activity(card_name, activity_data)
        add_activity_window.destroy()
        display_activity_detail(card_name)  # Refresh the activity list after adding


    add_activity_button = tk.Button(add_activity_window, text="Add Activity", command=add_activity)
    add_activity_button.pack(padx=10, pady=10)


def save_activity(card_name, activity_data):
    activities = load_activities(card_name)
    activities.append(activity_data)
    save_activities(card_name, activities)
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

    Checking_button = tk.Button(navbar_frame, text="Checking", bg="white", fg="black", padx=10, pady=5,
                               command=lambda: select_option("Checking"))
    Checking_button.pack(side=tk.LEFT, padx=10, pady=10)

    global welcome_label
    welcome_label = tk.Label(root, text="", font=("Arial", 18))
    welcome_label.pack(pady=50)

    card_info_frame = tk.Frame(root)  # Frame for displaying card information

    display_home()

    root.mainloop()

if __name__ == "__main__":
    create_menu()
