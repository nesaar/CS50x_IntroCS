from cs50 import get_string


def main():
    # Get the card number
    cardno = get_string("Card number: ")

    # check the card type now
    cardtype = checkcardtype(cardno)

    # check if the number is valid if the card type is valid
    if cardtype != "INVALID":
        if checkvalidnumber(cardno):
            print(cardtype)
        else:
            print("INVALID")
    else:
        print(cardtype)


def checkcardtype(cardno):
    # get card length and store
    cardlen = len(cardno)

    # now check card length and first digit check
    if (cardlen == 13 or cardlen == 16) and cardno[:1] == "4":
        return "VISA"
    elif (cardlen == 16) and (cardno[:1] == "5" and cardno[1:2] in ("1", "2", "3", "4", "5")):
        return "MASTERCARD"
    elif (cardlen == 15) and (cardno[:1] == "3" and cardno[1:2] in ("4", "7")):
        return "AMEX"
    else:
        return "INVALID"


def checkvalidnumber(cardno):
    # to keep the sum of the digits
    nSum = 0

    # to track the 2nd digit from the right
    bSecond = 0

    # to track the index from right to left
    nIndex = -1

    # card number length
    clen = len(cardno)

    # traverse the card number but in reverse starting the right and working to the left
    for i in range(clen-1, -1, -1):
        # get the digit we are working with
        d = int(cardno[i])

        if bSecond == 1:
            d = d * 2
            bSecond = 0

        nSum = nSum + (d / 10)
        nSum = nSum + (d % 10)

    return (nSum % 10 == 0)


if __name__ == "__main__":
    main()