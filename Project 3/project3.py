import os
import tkinter as tk
import json
from tkinter import ttk
from datetime import datetime
from tkinter import ttk
from tkcalendar import Calendar
import tkinter.messagebox as messagebox
import calendar


ACTIVITIES_FOLDER = "activities"

if not os.path.exists(ACTIVITIES_FOLDER):
    os.makedirs(ACTIVITIES_FOLDER)

def update_activity_tree(activity_tree, card_name, activity_data):
    # Load the updated activities and clear the current treeview
    activity_tree.delete(*activity_tree.get_children())
    activities = load_activities(card_name)

    # Insert updated activities into the treeview
    for activity in activities:
        activity_tree.insert("", "end", values=(activity['date'], activity['amount'], activity['type'], activity['description']))

# Function remains unchanged
def add_activity():
    if detail_frame.winfo_ismapped():
        selected_item = card_tree.focus()
        card_name = card_tree.item(selected_item)['values'][0]
        display_activity_detail(card_name)

def create_calendar(root):
    # Get the current date
    today = datetime.now()
    current_year = today.year
    current_month = today.month

    # Get the month's name
    month_name = today.strftime("%B")

    # Create a calendar for the current month
    cal = calendar.monthcalendar(current_year, current_month)

    # Create a frame to display the calendar
    calendar_frame = tk.Frame(root)
    calendar_frame.pack()

    # Add the month's name at the top
    month_label = tk.Label(calendar_frame, text=month_name, font=("Arial", 14, "bold"))
    month_label.grid(row=0, columnspan=7)  # Span across all columns

    # Create weekday labels
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day_label_width = 8  # Adjust width as needed
    for day in weekdays:
        label = tk.Label(calendar_frame, text=day, width=day_label_width, borderwidth=2, relief="solid")
        label.grid(row=0, column=weekdays.index(day))

    # Read card information from cards.json
    try:
        with open("cards.json", "r") as file:
            card_info = json.load(file)
    except FileNotFoundError:
        card_info = []

    # Convert due dates to integers for comparison
    card_due_dates = {int(card['due_date']): card['name'] for card in card_info}
    min_card_width = 10

    # Display calendar days and card due dates
    for week_num, week in enumerate(cal):
        for weekday, day in enumerate(week):
            if day != 0:
                # Get the width of the day header label
                day_header_width = label.winfo_reqwidth()

                day_frame = tk.Frame(calendar_frame, width=day_header_width, height=60, borderwidth=2, relief="solid")
                day_frame.grid(row=week_num + 1, column=weekday)

                day_label = tk.Label(day_frame, text=str(day))
                day_label.pack()

                # Check if the day matches a card due date and display it with balance-based colors
                if day in card_due_dates:
                    card_name = card_due_dates[day]
                    matching_cards = [card for card in card_info if card['name'] == card_name]
                    if matching_cards:
                        card_info_for_day = matching_cards[0]
                        balance = float(card_info_for_day['balance'].replace('$', ''))
                        if balance <= 0:
                            card_label = tk.Label(day_frame, text=card_name.ljust(min_card_width), bg="lightgreen")
                        else:
                            card_label = tk.Label(day_frame, text=card_name.ljust(min_card_width), bg="lightcoral")
                        card_label.pack()

                # Add invisible labels to fill up the space
                else:
                    empty_label = tk.Label(day_frame, text="_________", bg=day_frame["bg"], fg=day_frame["bg"])
                    empty_label.pack()

def display_home():
    welcome_label.config(text="Welcome to Finance Tracker!")
    remove_calendar()
    create_calendar(root)

def remove_calendar():
    # Find and destroy the calendar frame if it exists
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget.winfo_children():
            # Check if this frame contains labels (calendar)
            children = widget.winfo_children()
            if isinstance(children[0], tk.Label) and children[0].cget("text").capitalize() in calendar.month_name:
                widget.destroy()
                break  
                      
def clear_label():
    welcome_label.config(text="")
    hide_cards()

def select_option(option):
    if option == "Home":
        hide_cards()
        display_home()
    elif option == "Cards":
        clear_label()
        remove_calendar()
        show_cards()
    else:
        clear_label()
        print(f"Selected: {option}")
    
    # Hide the detail frame when any navigation button is clicked, if it exists
    detail_frame.pack_forget()


def show_cards():
    card_info_frame.pack(side=tk.TOP)
    load_cards()

def hide_cards():
    card_info_frame.pack_forget()

def load_cards():
    try:
        with open("cards.json", "r") as file:
            card_info = json.load(file)
            display_cards(card_info)
    except FileNotFoundError:
        display_cards([])

def get_card_info_by_name(card_name):
    try:
        with open("cards.json", "r") as file:
            card_info = json.load(file)
            for card in card_info:
                if card['name'] == card_name:
                    return card
    except FileNotFoundError:
        return None

def update_card_details(original_card_name, new_name, new_due_date):
    try:
        with open("cards.json", "r") as file:
            card_info = json.load(file)
    except FileNotFoundError:
        card_info = []
        
    if any(card['name'] == new_name for card in card_info if card['name'] != original_card_name):
        messagebox.showerror("Error", f"Card with name '{new_name}' already exists.")
        return False

    # Find the card to be updated
    for card in card_info:
        if card['name'] == original_card_name:
            # Update the card details
            card['name'] = new_name
            card['due_date'] = new_due_date
            break

    # Save the updated card information back to cards.json
    back_to_cards()  # Unload the detail page
    save_cards(card_info)

    # Optionally, update the associated activities filename if the card name has changed
    if original_card_name != new_name:
        try:
            old_activities_file = os.path.join(ACTIVITIES_FOLDER, f"{original_card_name}_activities.json")
            new_activities_file = os.path.join(ACTIVITIES_FOLDER, f"{new_name}_activities.json")
            os.rename(old_activities_file, new_activities_file)
        except FileNotFoundError:
            pass  



def display_activity_detail(card_name):
    hide_cards()

    global detail_frame
    detail_frame = tk.Frame(root)
    detail_frame.pack(fill=tk.BOTH, expand=True)

    card_info = get_card_info_by_name(card_name)
    due_date = card_info['due_date']

    # New label to display card name and due date
    card_info_label = tk.Label(detail_frame, text=f"Credit Card: {card_name}\nDue Date: {due_date}", font=("Arial", 12, "bold"))
    card_info_label.pack()

    # Frame for buttons above the table
    button_frame = tk.Frame(detail_frame)
    button_frame.pack(fill=tk.X)

    def edit_card_details():
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Card Details")

        name_label = tk.Label(edit_window, text="Name:")
        name_label.pack(padx=10, pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.insert(tk.END, card_name)  # Set initial value to current card name
        name_entry.pack(padx=10, pady=5)

        due_date_label = tk.Label(edit_window, text="Due Date (DD):")
        due_date_label.pack(padx=10, pady=5)
        cal = Calendar(edit_window, selectmode="day", date_pattern="dd/MM/yyyy")
        cal.pack(padx=10, pady=5)

        # Extract day value from the due_date
        due_day = int(due_date)

        # Get today's date
        today = datetime.now()

        # Calculate the closest date to the current date with the same day value
        if due_day >= today.day:
            closest_date = today.replace(day=due_day)
        else:
            if today.month == 12:
                closest_date = today.replace(year=today.year + 1, month=1, day=due_day)
            else:
                closest_date = today.replace(month=today.month + 1, day=due_day)

        # Set the calendar date to the closest date
        cal_date = closest_date.strftime("%d/%m/%Y")
        cal.selection_set(cal_date)

        def update_card():
            new_name = name_entry.get()
            new_due_date = cal.get_date().split("/")[0]
            # Update the card details
            if update_card_details(card_name, new_name, new_due_date):
                # Update the display to reflect the changes only if the update was successful
                display_activity_detail(new_name)
            edit_window.destroy()


        update_button = tk.Button(edit_window, text="Update", command=update_card)
        update_button.pack(padx=10, pady=10)


    edit_button = tk.Button(button_frame, text="Edit", command=edit_card_details, bg="Light Blue")
    edit_button.pack(side=tk.LEFT, padx=10, pady=10)

    delete_button = tk.Button(button_frame, text="Delete", command=back_to_cards, bg="Red")
    delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

    activities = load_activities(card_name)

    table_frame = tk.Frame(detail_frame)
    table_frame.pack(expand=True)

    activity_tree = ttk.Treeview(table_frame, columns=("Date", "Amount", "Description", "Type"), show="headings")
    activity_tree.heading("Date", text="Date")
    activity_tree.heading("Amount", text="Amount")
    activity_tree.heading("Description", text="Description")
    activity_tree.heading("Type", text="Type")

    for activity in activities:
        activity_tree.insert("", "end", values=(activity['date'], "$" + activity['amount'], activity['description'], activity['type']))

    activity_tree.pack(fill=tk.BOTH, expand=True)
    table_frame.pack(expand=True, padx=10, pady=(0, 0), fill=tk.BOTH)

    back_button = tk.Button(detail_frame, text="Back", command=back_to_cards, bg="grey")
    back_button.pack(side=tk.LEFT, padx=10, pady=10, anchor="sw")

    add_activity_button = tk.Button(detail_frame, text="Add Activity", command=lambda: display_add_activity_prompt(card_name, activity_tree), bg="green")
    add_activity_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="se")


    # Calculating totals for credit and debit
    credit_total = 0
    debit_total = 0

    for activity in activities:
        amount = float(activity['amount'].replace('$', ''))
        if activity['type'] == 'Credit (-)':
            credit_total += amount
        elif activity['type'] == 'Debit (+)':
            debit_total += amount
    # Calculate total balance by adding credit and subtracting debit
    total_balance = credit_total - debit_total

    # Update the corresponding credit card balance in cards.json
    update_card_balance(card_name, total_balance)

    total_frame = tk.Frame(detail_frame)
    total_frame.pack(side=tk.BOTTOM, padx=10)

    total_label = tk.Label(total_frame, text=f"Total Balance: ${total_balance:.2f}", font=("Arial", 12))
    total_label.pack(side=tk.BOTTOM, padx=10)

def back_to_cards():
    detail_frame.pack_forget()
    show_cards()

def update_card_balance(card_name, new_balance):
    try:
        with open("cards.json", "r") as file:
            card_info = json.load(file)
    except FileNotFoundError:
        card_info = []

    # Update the balance for the corresponding card
    for card in card_info:
        if card['name'] == card_name:
            card['balance'] = f"${new_balance:.2f}"
            break

    # Save the updated card information back to cards.json
    save_cards(card_info)


def load_activities(card_name):
    try:
        file_path = os.path.join(ACTIVITIES_FOLDER, f"{card_name}_activities.json")
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_activities(card_name, activities):
    file_path = os.path.join(ACTIVITIES_FOLDER, f"{card_name}_activities.json")
    with open(file_path, "w") as file:
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

    card_tree.bind("<Double-1>", on_select_card)
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
    
    cal = Calendar(add_card_window, selectmode="day", date_pattern="dd/MM/yyyy")
    cal.pack(padx=10, pady=5)

    def get_due_date():
        due_date = cal.get_date().split("/")[0]
        add_card(name_entry.get(), due_date, add_card_window)

    add_button = tk.Button(add_card_window, text="Add Card", command=get_due_date)
    add_button.pack(padx=10, pady=10)

def add_card(name, due_date, window):
    try:
        with open("cards.json", "r") as file:
            card_info = json.load(file)
            # Check for duplicate card names before adding
            if any(card['name'] == name for card in card_info):
                messagebox.showerror("Error", f"Card with name '{name}' already exists.")
                return
            save_activities(name, [])
    except FileNotFoundError:
        card_info = []
    card_info.append({"name": name, "balance": "$0.00", "due_date": due_date})
    save_cards(card_info)
    display_cards(card_info)
    window.destroy()  

def save_cards(card_info):
    with open("cards.json", "w") as file:
        json.dump(card_info, file, indent=4)


def display_add_activity_prompt(card_name, activity_tree):
    add_activity_window = tk.Toplevel(root)
    add_activity_window.title(f"Add Activity for {card_name}")

    date_label = tk.Label(add_activity_window, text="Date:")
    date_label.pack(padx=10, pady=5)
    cal = Calendar(add_activity_window, selectmode="day", date_pattern="dd/MM/yyyy")
    cal.pack(padx=10, pady=5)

    def validate_amount_input(value):
        if value == "":
            return True
        try:
            if '.' not in value:
                float(value + '.00')
                return True
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
    type_var.set("Credit (-)")
    type_dropdown = tk.OptionMenu(add_activity_window, type_var, "Credit (-)", "Debit (+)")
    type_dropdown.pack(padx=10, pady=5)

    description_label = tk.Label(add_activity_window, text="Description:")
    description_label.pack(padx=10, pady=5)
    description_entry = tk.Entry(add_activity_window)
    description_entry.pack(padx=10, pady=5)

    def add_activity():
        entered_amount = amount_entry.get()
        if '.' not in entered_amount:
            entered_amount += '.00'

        activity_data = {
            "date": cal.get_date(),
            "amount": entered_amount,
            "type": type_var.get(),
            "description": description_entry.get()
        }

        save_activity(card_name, activity_data)
        update_activity_tree(activity_tree, card_name, activity_data)
        add_activity_window.destroy()
        back_to_cards()
        display_activity_detail(card_name)

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
    root.geometry("1080x800")

    navbar_frame = tk.Frame(root, bg="black")
    navbar_frame.pack(fill=tk.X)

    home_button = tk.Button(navbar_frame, text="Home", bg="white", fg="black", padx=10, pady=5,
                            command=lambda: select_option("Home"))
    home_button.pack(side=tk.LEFT, padx=10, pady=10)

    cards_button = tk.Button(navbar_frame, text="Cards", bg="white", fg="black", padx=10, pady=5,
                             command=lambda: select_option("Cards"))
    cards_button.pack(side=tk.LEFT, padx=10, pady=10)

    global welcome_label
    welcome_label = tk.Label(root, text="", font=("Arial", 18))
    welcome_label.pack(pady=50)

    card_info_frame = tk.Frame(root)

    display_home()

    root.mainloop()

if __name__ == "__main__":
    create_menu()
