#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


bool key_is_valid();

int main(int argc, string argv[])
{
    //Exiting with code 1 if less than 2 args entered.
    if (argc < 2)
    {
        printf("Usage: ./substitution key\n");
        exit(1);
    }

    string key = argv[1];
    int key_length = strlen(argv[1]);

    bool is_valid = key_is_valid(key, key_length);

    //if function(key_is_valid) returned true we are proceeding with next steps
    if (is_valid)
    {
        string plain_text = get_string("plain text: ");
        int plain_text_len = strlen(plain_text);

        printf("ciphertext: ");
        for (int i = 0; i < plain_text_len; i++)
        {
            char cipher;
            char cipher_text;
            //checking if the plain text has symbols
            if (!isalpha(plain_text[i]))
            {
                printf("%c", plain_text[i]);
                continue;
            }
            //checking if letter in plain text is uppercase
            else if (isupper(plain_text[i]))
            {
                cipher = key[plain_text[i] - 'A'];
                cipher_text = cipher;
                printf("%c", toupper(cipher_text));
            }
            //checking if letter in plain text is lowercase
            else if (islower(plain_text[i]))
            {
                cipher = key[plain_text[i] - 'a'];
                cipher_text = cipher;
                printf("%c", tolower(cipher_text));
            }

        }
        //printing empty line
        printf("\n");
    }
    else
    {
        return 1;
    }
}

//Checking if the key is valid
bool key_is_valid(string key, int key_length)
{
    if (key_length < 26 || key_length > 26)
    {
        printf("Key must contain 26 characters.\n");
        return false;
    }

    //checking if there are duplicated letters in key
    for (int i = 0; i < key_length - 1; i++)
    {
        for (int j = i + 1; j < key_length; j++)
        {
            if (key[i] == tolower(key[j]) || key[i] == toupper(key[j]))
            {
                printf("Key must not contain repeated characters.\n");
                return false;
            }
            //checking if digits are in key
            else if (isdigit(key[i]))
            {
                printf("Key must only contain alphabetic characters.\n");
                return false;
            }
        }
    }
    //returning true if everything is okay
    return true;
}