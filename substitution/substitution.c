#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>

string encrypttext(string input, string cypher)
{
    string alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string chartocypher;
    string cyphertext = input;

    int charlocation = 0;
    int n = strlen(input);
    int cypherloc = 0;

    bool isFound = 0;
    bool isUpper = 0;

    //loop through the provided string
    for (int i = 0; i < n; i++)
    {
        //reset the counters needed
        isFound = 0;
        cypherloc = -1;
        isUpper = !islower(input[i]);

        //now for each character in the string find the corresponding cypher character
        while ((!isFound) && (cypherloc < 52))
        {
            cypherloc++;

            if (input[i] == alphabet[cypherloc])
            {
                isFound = 1;
            }
        }

        if (isFound)
        {
            if (cypherloc > 25)
            {
                cypherloc = (cypherloc - 26);
            }

            if (isUpper)
            {
                cyphertext[i] = toupper(cypher[cypherloc]);
            }
            else
            {
                cyphertext[i] = tolower(cypher[cypherloc]);
            }
        }
        else
        {
            cyphertext[i] = input[i];
        }
    }

    return cyphertext;
}

int main(int argc, string argv[])
{
    //check the arguments passed to the program
    //no argument passed
    if ((argc <= 1) || (argc > 2))
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if ((argc == 0) || (argc > 2))
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    //less or more than 26 characters passed
    if (strlen(argv[1]) < 26 || strlen(argv[1]) > 26 || strlen(argv[1]) == 0)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    //check for non-alphabet characters
    string cs = argv[1];
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (cs[i] < 'A' || cs[i] > 'z' || (cs[i] < 'a' && cs[i] > 'Z'))
        {
            printf("Key must contain 26 alphabet characters.\n");
            return 1;
        }
    }
    //check for duplicates of the same letter
    for (int i = 0, n = strlen(cs); i < n; i++)
    {
        int dupcount = 0;
        for (int j = i + 1; cs[j] != '\0'; j++)
        {
            if (cs[i] == cs[j])
            {
                dupcount++;
            }
        }
        if (dupcount >= 1)
        {
            printf("Key must contain 26 unique alphabet characters.\n");
            return 1;
        }
    }

    //get the cypher from the argument passed to the program
    string cypher = argv[1];

    //get the text the user wants to encrypt
    string plaintext = get_string("plaintext: ");

    //encrypt the text
    string cyphertext = encrypttext(plaintext, cypher);

    //show the cyphertext
    printf("ciphertext: %s\n", cyphertext);

    return 0;
}