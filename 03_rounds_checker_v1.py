def check_rounds(min_value, max_value):
    error = "Please enter a whole number that is more " \
            "than 0 and less than 114"

    try:
        response = int(input("Choose a number: "))

        if response < min_value or response > max_value:
            print(error)
        else:
            return response

    except ValueError:
        print(error)


# *** Main Routine ***

while True:
    to_check = check_rounds(1, 113)
    print("Success")