from datetime import datetime

	print("Hello. What is your birthday(MM-DD-YYYY)?")
	myBirthday = input()

try:
	birthday = datetime.strptime(myBirthday, "%m-%d-%Y")
execept: ValueError:
	print("Please input a birthday in the valid format 'MM-DD-YYYY'.")
else:
	current_date = datetime.now()
	age_in_seconds = (current_date - birthday).total_seconds()

	print("You are approximately {age_in_seconds} seconds old.")
