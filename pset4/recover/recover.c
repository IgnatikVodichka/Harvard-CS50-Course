#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Usage: ./recover forensic image\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");

    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    //declaring our veriables
    char name[8];
    BYTE buffer[512];
    FILE *output = NULL;
    int count = 0;

    // doing following steps untill the condition on the bottom will be satisfied
    do
    {
        //check to see if it's a JPG indeed.
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (count == 0)
            {
                sprintf(name, "%03i.jpg", count);
                output = fopen(name, "w");
                fwrite(buffer, sizeof(buffer), 1, output);
                count++;
            }
            // if it's another one
            else if (count > 0)
            {
                fclose(output);

                sprintf(name, "%03i.jpg", count);
                output = fopen(name, "w");
                fwrite(buffer, sizeof(buffer), 1, output);
                count++;
            }
        }
        // if it's not the first one continue
        else
        {
            if (output != NULL)
            {
                fwrite(buffer, sizeof(buffer), 1, output);
            }
        }

    } // condition which shoud suffice before ending loop
    while (fread(buffer, sizeof(buffer), 1, input) != 0);

    fclose(output);
    fclose(input);
}