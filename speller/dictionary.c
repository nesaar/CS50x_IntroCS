// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

int dictionary_size = 0;

// to check if i can compile this code without any issues
// before going to make speller.c
//int main(void)
//{
//
//}

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{

    // first hash the word we are looking for
    int hashv = hash(word);

    // navigate to this value in the table
    node *dw = table[hashv];

    // look for the word now
    while (dw != NULL)
    {
        if (strcasecmp(word, dw->word) == 0)
        {
            // word was found
            return true;
        }

        dw = dw->next;
    }

    // we did not find the word so return false
    return false;
}

// Hashes word
unsigned int hash(const char *word)
{
    // Improve this hash function
    // use the ascii foundation for each char in the word
    int hsum = 0;

    for (int i = 0, j = strlen(word); i < j; i++)
    {
        hsum = hsum + toupper(word[i]);
    }

    hsum = hsum % N;

    return hsum;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the names dictionary file
    FILE *dictionaryp = fopen(dictionary, "r");
    if (dictionaryp == NULL)
    {
        printf("Unable to open %s/n", dictionary);
        return false;
    }

    // create the word variable to read the dictionary words in 1 by 1
    char dictword[LENGTH + 1];

    while (fscanf(dictionaryp, "%s", dictword) != EOF)
    {
        node *dw = malloc(sizeof(node));
        if (dw == NULL)
        {
            return false;
        }

        // put the word in dictword from the dictionary into the node
        strcpy(dw->word, dictword);

        // now hash the word
        int hash_value = hash(dictword);

        // store the hashed value into the struct
        dw->next = table[hash_value];
        table[hash_value] = dw;
        dictionary_size++;
    }

    fclose(dictionaryp);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dictionary_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Free each element in the hash table
    // This was created as *dw in the LOAD
    for (int i = 0; i < N; i++)
    {
        // Assign cursor
        node *dw = table[i];

        // Loop through linked list
        while (dw != NULL)
        {
            // Make temp equal cursor;
            node *tmp = dw;
            dw = dw->next;

            // free temp
            free(tmp);
        }

        // check if anything is left or we have reached the max
        if (dw == NULL && i == N - 1)
        {
            return true;
        }
    }

    return false;
}