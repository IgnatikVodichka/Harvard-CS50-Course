#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start_size;
    do
    {
        start_size = get_int("Positive integer greater than 9(Start size): ");
    }
    while (start_size < 9);

    // TODO: Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("Positive integer greater than 9(End size): ");
    }
    while (end_size < start_size);

    // TODO: Calculate number of years until we reach threshold
    int n_years = 0;
    while (start_size < end_size)
    {
        start_size = start_size + (start_size / 3) - (start_size / 4);
        n_years++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", n_years);
}