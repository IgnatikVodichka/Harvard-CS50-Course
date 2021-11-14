#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // taking an input from a user
    string text = get_string("Text: ");

    double number_of_letters = count_letters(text);
    double number_of_words = count_words(text);
    double number_of_sentences = count_sentences(text);

    double L = (number_of_letters / number_of_words) * 100; //average number of letters per 100 words

    double S = (number_of_sentences / number_of_words) * 100; //average number of sentences per 100 words

    double index = 0.0588 * L - 0.296 * S - 15.8;

    int intindex = round(index); //rounding up and cutting off zeroes

    //if, else statements to check what grade is it.
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (intindex > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", intindex);
    }
}

int count_letters(string text) //counting letters
{
    int letter_count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        int letter = tolower(text[i]);

        if (letter >= 97 & letter <= 122)
        {
            letter_count ++;
        }
    }

    return letter_count;
}

int count_words(string text) //counting words
{
    int word_count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        int letter = text[i];

        if (letter == 32)
        {
            word_count ++;
        }
    }

    return word_count + 1;
}

int count_sentences(string text) //counting sentences
{
    int sentence_count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        int letter = text[i];

        if (letter == 21 || letter == 46 || letter == 63)
        {
            sentence_count ++;
        }
    }

    return sentence_count;
}