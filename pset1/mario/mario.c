#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Geting Number of height from user
    int height;
    do
    {
        height = get_int("Positive integer greater than 0(Start size): ");
    }
    while (height < 1 || height > 8);

    //Creating for loop to make staircase
    for (int i = 0; i < height; i++)
    {
        //We printing no. of empty spaces minus 1 each time
        int s = height - (i + 1);
        for (int j = 0; j < s; j++)
        {
            printf(" ");
        }

        //We printing no. of # minus 1 each time
        int pattern = i + 1;
        for (int j = 0; j < pattern; j++)
        {
            printf("#");
        }

        for (int j = 0; j < 2; j++)
        {
            printf(" ");
        }

        for (int j = 0; j < pattern; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}