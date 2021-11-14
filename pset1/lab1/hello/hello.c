#include <stdio.h>
#include <cs50.h>

int main(void)
// Prints "Hello, World!", and then saks for user's name and prints "Hello, (user's name)"
{
    printf("Hello, World!\n");

    string name = get_string("What's your name, sir?\n");
    printf("Hello, %s\n", name);
}

