#include <cs50.h>
#include <stdio.h>


int main(void)
{
    long creditcard_number; // our credit card number
    int first_digit; // will write here our first digit
    int first_two_digit; // will write here our first 2-3 digits
    int sum_of_two_digit = 0; // sum of our number if multiplied by two will be greater then 10
    int sum_of_everyother_digit = 0;
    int sum_of_other_digit = 0; // sum of rest of the digits
    int sum_of_all_digit = 0;
    int digit_counter = 0; // will keep track how many digit's are there

    do
    {
        creditcard_number = get_long("Credit card number: ");
    }
    while (creditcard_number < 0);

    first_two_digit = creditcard_number / 10000000000000;

    while (creditcard_number != 0)
    {
        int digit = creditcard_number % 10;
        creditcard_number /= 10;
        digit_counter++;
        first_digit = digit;

        if (digit_counter % 2 == 0)
        {
            digit *= 2;

            if (digit >= 10)
            {
                while (digit != 0)
                {
                    int n = digit % 10;
                    sum_of_two_digit += n;
                    digit /= 10;
                }
            }
            sum_of_everyother_digit += digit;
        }
        else
        {
            sum_of_other_digit += digit;
        }
    }

    sum_of_everyother_digit += sum_of_two_digit;
    sum_of_all_digit = sum_of_other_digit + sum_of_everyother_digit;



    // printf("First two digits:%i\n", first_two_digit);
    // printf("Quantity of digits in this number is:%i\n", digit_counter);
    // printf("Sum of everyother digit is:%i\n", sum_of_everyother_digit);
    // printf("Sum of other digit is:%i\n", sum_of_other_digit);
    // printf("Sum of all digit is:%i\n", sum_of_all_digit);
    // printf("First digit is:%i\n", first_digit);

    if (first_digit == 3 & sum_of_all_digit % 10 == 0 & digit_counter == 15)
    {
        if (first_two_digit == 34 || first_two_digit == 37)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }

    }

    else if (first_digit == 4 & sum_of_all_digit % 10 == 0 & (digit_counter == 13 || digit_counter == 16))
    {
        printf("VISA\n");
    }

    else if (first_digit == 5 & sum_of_all_digit % 10 == 0 & digit_counter == 16)
    {
        if (first_two_digit / 10 > 50 & first_two_digit / 10 < 56)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }


}