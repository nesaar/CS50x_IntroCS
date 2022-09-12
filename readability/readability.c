#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int numberOfSentences = 0;
int numberOfWords = 0;
int numberOfLetters = 0;
int numberOfSpaces = 0;
int numberOfPunc = 0;

//analyse the string and break it up into the parameters required by the calculation
void analyse(string input)
{
    //loop through the string 1 char at a time
    for (int i = 0, n = strlen(input); i < n; i++)
    {
        //check for letters of the alphabet both upper and lower case
        if ((input[i] >= 'a' && input[i] <= 'z') || (input[i] >= 'A' && input[i] <= 'Z'))
        {
            numberOfLetters++;
        }

        //check a space
        if (input[i] == ' ')
        {
            numberOfSpaces++;
            numberOfWords++;
        }

        //check for the end of a sentence
        if (input[i] == '.' || input[i] == '!' || input[i] == '?')
        {
            numberOfPunc++;
            numberOfSentences++;
        }
    }

    //catch the last word in the sentence that is not followed by a space
    numberOfWords++;
}

int ColemanCalc()
{
    // L is the average number of letters per 100 words in the text. Using 1.00 to force to float
    float L = ((numberOfLetters * 1.00) / (numberOfWords * 1.00)) * 100;

    //S is the average number of sentences per 100 words in the text. Using 1.00 to force to float
    float S = ((numberOfSentences * 1.00) / (numberOfWords * 1.00)) * 100;

    /*
    printf("S: %f\n", S);
    printf("L: %f\n", L);
    printf("\n");
    */

    float result = (0.0588 * L) - (0.296 * S) - 15.8;
    //printf("Calc: %f\n", round(result));

    return round(result);
    //printf("\n");
}

int main(void)
{
    // get the input text
    string input = get_string("Text: ");

    // break the sentence into words, letters, sentences
    analyse(input);

    /*
    printf("Sentences: %i\n", numberOfSentences);
    printf("Words: %i\n", numberOfWords);
    printf("Letters: %i\n", numberOfLetters);
    printf("Spaces: %i\n", numberOfSpaces);
    printf("Punctuation: %i\n", numberOfPunc);
    printf("\n");
    */

    // perform the Coleman-Coleman-Liau calculation
    int grade = ColemanCalc();
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}