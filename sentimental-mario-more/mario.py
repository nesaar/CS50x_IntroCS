from cs50 import get_int


# function to print the leading spaces plus the trailing hash
def printrow(height, n):
    # handle the base case
    if height == 0:
        return False

    # recursively print the half pyramid
    print(" " * (height - 1) + "#" * n + "  " + "#" * n)
    printrow(height - 1, n + 1)

    return True


# get the user input and make sure it is valid
while(True):
    height = get_int("Height: ")

    # check for height validity
    if int(height) < 1 or int(height) > 8:
        print("Height must be between 1 and 8")
    elif int(height) > 0 and int(height) < 9:
        printrow(height, 1)
        break