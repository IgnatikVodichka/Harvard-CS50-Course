// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>
#include <strings.h>
#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

int free_dictionary(node *next);

// Number of buckets in hash table
const unsigned int N = 57;

// Hash table
node *table[N];
int qty_of_words = 0;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //opening file to read from
    FILE *dictfile = fopen(dictionary, "r");
    char word[LENGTH + 1];

    if (dictfile == NULL)
    {
        return false;
    }

    //scanning the file word by word untill end of the file
    while (fscanf(dictfile, "%s", word) != EOF)
    {
        //allocating memory for new node each time the loop passes
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        else
        {
            //copying string(word) from file to node
            strcpy(n->word, word);

            n->next = NULL;

            int hash_index = hash(word);

            //if the place is vacant allocating pointer to table
            if (table[hash_index] == NULL)
            {
                table[hash_index] = n;
                qty_of_words++;
            }

            //if the place is occupied then we insert new value into linked list
            else
            {
                n = table[hash_index];
                table[hash_index] = n;
                qty_of_words++;
            }
        }
    }
    fclose(dictfile);

    return true;
}

// Hashes word to a number
// djb2 hash function from http://www.cse.yorku.ca/~oz/hash.html
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;

    int c = *word;
    c = tolower(c);

    while (*word != 0)
    {
        hash = ((hash << 5) + hash) + c;
        c = *word++;
        c = tolower(c);
    }
    hash = hash % N;

    return hash;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);

    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor -> word, word) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;

}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return qty_of_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            node *tmp = table[i] -> next;
            free(table[i]);
            table[i] = tmp;
        }

    }

    return true;
}