import os  # Import the 'os' module to clear the console

def calculate_expression(expression):
    try:
        return eval(expression)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {str(e)}"

def reset_variables():
    global current_equation, expression_parts, expecting_number, entry_count, equals_allowed, equation_finished
    current_equation = ''
    expression_parts = []
    expecting_number = True
    entry_count = 0
    equals_allowed = False
    equation_finished = False

def again():
    calc_again = input('''
Do you want to calculate again?
Please type Y for YES or N for NO.
''')

    if calc_again.upper() == 'Y':
        reset_variables()  # Reset variables to default values
    elif calc_again.upper() == 'N':
        print('See you later.')
        exit() # Please leave now, please work.
    else:
        again()

reset_variables()  # Reset variables to default values

while True:
    if expecting_number:
        user_input = input("Enter a number: ")
    elif len(expression_parts) >= 3:
        user_input = input("Enter an operator (+, -, *, /) or '=': ")
    else:
        user_input = input("Enter an operator (+, -, *, /): ")

    if user_input == '=':
        if not equals_allowed:
            print("Invalid input. '=' is not allowed at this point.")
        elif len(expression_parts) < 3 or len(expression_parts) % 2 == 0:
            print("Invalid expression. It must end with a number and have at least 3 entries.")
        else:
            equation = ' '.join(map(str, expression_parts))
            result = calculate_expression(''.join(map(str, expression_parts)))
            print(f"\nEquation: {equation}")
            print(f"Result: {result}\n")
            again()
        continue  # Continue the loop without breaking
    elif equation_finished:
        print("Invalid input. Equation is already finished.")
        continue  # Continue the loop without breaking
    elif user_input in ('+', '-', '*', '/'):
        if expecting_number:
            print("Invalid input. Operator was not expected.")
        else:
            expression_parts.append(user_input)
            expecting_number = True
    else:
        try:
            num = float(user_input)
            if expecting_number:
                expression_parts.append(num)
                entry_count += 1  # Increment entry count when adding a number
                expecting_number = False
            else:
                print("Invalid input. Number was not expected.")
        except ValueError:
            if expecting_number:
                print("Invalid input. Please enter a number.")
            else:
                print("Invalid input. Please enter an operator.")

    # Update the equals_allowed flag based on the conditions
    if entry_count >= 2 and not equation_finished:
        equals_allowed = True
    else:
        equals_allowed = False

    # Print current equation with extra spaces
    current_equation = ' '.join(map(str, expression_parts))
    print(f"\nCurrent Equation: {current_equation}\n")

calculate_expression
