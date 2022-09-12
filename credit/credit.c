#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//works out what the possible card type is
string cardtype(string sCNo, int numberlength)
{
    //work out if its an AMEX card even though the number could still be invalid
    if (((numberlength == 13) || (numberlength == 16)) && (sCNo[0] == '4'))
    {
        return "VISA";
    }
    //work out if its a A card even though the number could still be invalid
    else if (numberlength == 16)
    {
        if ((sCNo[0] == '5') && ((sCNo[1] == '1') || (sCNo[1] == '2') || (sCNo[1] == '3') || (sCNo[1] == '4') || (sCNo[1] == '5')))
        {
            return "MASTERCARD";
        }
    }
    //work out if its a AMEX card even though the number could still be invalid
    else if (numberlength == 15)
    {
        if ((sCNo[0] == '3') && ((sCNo[1] == '4') || (sCNo[1] == '7')))
        {
            return "AMEX";
        }
    }

    //if it does not fit into any of the above then it is already an INVALID card
    return "INVALID";
}

bool checknumbervalidity(string cardnumber, int numberlength)
{
    int nSum = 0, isSecond = false;

    //loop through all the digits of the number starting at the right
    for (int i = numberlength - 1; i >= 0; i--)
    {
        int d = cardnumber[i] - '0';

        // its the second digit from the right so this must be doubled
        if (isSecond == true)
        {
            d = d * 2;
        }

        // We add two digits to handle cases that make two digits after doubling
        nSum += d / 10;
        nSum += d % 10;

        isSecond = !isSecond;
    }

    return (nSum % 10 == 0);
}

int main(void)
{
    //get the card number from the user
    long cardnumber = get_long("Number: ");

    //work out the length of the card number
    int numberlength = snprintf(NULL, 0, "%lu", cardnumber);

    //convert the card number to a "string" for manipulation
    char cCardnumber [numberlength];
    sprintf(cCardnumber, "%lu", cardnumber);
    string sCardnumber = cCardnumber;

    //work out the card type before even continuing
    string sCardtype = cardtype(sCardnumber, numberlength);
    int ncomp = strcmp(sCardtype, "INVALID");

    if (ncomp != 0)
    {st
        if (checknumbervalidity(sCardnumber, numberlength))
        {
            printf("%s\n", sCardtype);
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("%s\n", sCardtype);
    }
}