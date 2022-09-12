#include <cs50.h>
#include <stdio.h>

void printrow(int row, int height)
{
    //setup the leading spaces
    int spaces = 1;
    while (spaces <= (height - row))
    {
        printf(" ");
        spaces++;
    }

    //setup the left side hash
    int hashes = 1;
    while (hashes <= row)
    {
        printf("#");
        hashes++;
    }

    //setup the middle spaces
    printf("  ");

    //setup the right side hash
    hashes = 1;
    while (hashes <= row)
    {
        printf("#");
        hashes++;
    }

    //end the line and move to the next line
    printf("\n");
}


int main(void)
{
    // Get the user input for pyramid height
    int height = 0;
    while (height < 1 || height > 8)
    {
        height = get_int("Height: ");
    }

    //print one row at a time
    //until the height is reached
    int i = 1;
    while (i <= height)
    {
        printrow(i, height);
        i++;
    }
}

