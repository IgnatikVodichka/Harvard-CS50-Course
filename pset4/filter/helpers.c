#include "helpers.h"
#include <math.h>


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //height loop
    for (int i = 0; i <= height; i ++)
    {
        //width loop
        for (int j = 0; j <= width; j ++)
        {
            //average of colors
            float average = round(image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3;
            image[i][j].rgbtRed = round(average);
            image[i][j].rgbtGreen = round(average);
            image[i][j].rgbtBlue = round(average);
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;

    //height loop
    for (int i = 0; i < height; i ++)
    {
        //width loop
        for (int j = 0; j < width / 2; j ++)
        {
            int k = width - 1;
            temp = image[i][j];
            image[i][j] = image[i][k - j];
            image[i][k - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //copying image
    RGBTRIPLE image_copy[height][width];

    for (int i = 0; i < height; i ++)
    {
        for (int j = 0; j < width; j ++)
        {
            image_copy[i][j] = image[i][j];
        }
    }

    //height loop
    for (int i = 0; i < height; i ++)
    {
        //width loop
        for (int j = 0; j < width; j ++)
        {
            int counter = 0;
            float sumOfRed = 0;
            float sumOfGreen = 0;
            float sumOfBlue = 0;

            //vertical loop for looking pixels vertically from target pixel
            for (int v = -1; v < 2; v++)
            {
                //horizontal loop for looking pixels horizontally from target pixel
                for (int h = -1; h < 2; h ++)
                {
                    //check if pixel vertically and horizontally are not out of array
                    if (i + v >= 0 && i + v <= (height - 1) && j + h >= 0 && j + h <= (width - 1))
                    {
                        //just the sum of all colors
                        sumOfRed += image_copy[i + v][j + h].rgbtRed;
                        sumOfGreen += image_copy[i + v][j + h].rgbtGreen;
                        sumOfBlue += image_copy[i + v][j + h].rgbtBlue;
                        counter++;
                    }
                }
            }

            //making original pixel of original image equal to that color of a copy pixel
            image[i][j].rgbtRed = round(sumOfRed / counter);
            image[i][j].rgbtGreen = round(sumOfGreen / counter);
            image[i][j].rgbtBlue = round(sumOfBlue / counter);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //declaring Gx matrix
    int Gx[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};

    //declaring Gy matrix
    int Gy[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};

    //copying image
    RGBTRIPLE image_copy[height][width];

    for (int i = 0; i < height; i ++)
    {
        for (int j = 0; j < width; j ++)
        {
            image_copy[i][j] = image[i][j];
        }
    }

    //height loop
    for (int i = 0; i < height; i ++)
    {
        //width loop
        for (int j = 0; j < width; j ++)
        {
            float GxRed = 0;
            float GxGreen = 0;
            float GxBlue = 0;

            float GyRed = 0;
            float GyGreen = 0;
            float GyBlue = 0;

            float productRed = 0;
            float productGreen = 0;
            float productBlue = 0;

            int k = 0;

            // vertical loop
            for (int v = -1; v < 2; v++)
            {
                //horizontal loop
                for (int h = -1; h < 2; h ++)
                {
                    if (i + v >= 0 && i + v <= (height - 1) && j + h >= 0 && j + h <= (width - 1))
                    {
                        GxRed += image_copy[i + v][j + h].rgbtRed * Gx[k];
                        GxGreen += image_copy[i + v][j + h].rgbtGreen * Gx[k];
                        GxBlue += image_copy[i + v][j + h].rgbtBlue * Gx[k];

                        GyRed += image_copy[i + v][j + h].rgbtRed * Gy[k];
                        GyGreen += image_copy[i + v][j + h].rgbtGreen * Gy[k];
                        GyBlue += image_copy[i + v][j + h].rgbtBlue * Gy[k];
                    }
                    k++;
                }
            }

            productRed = round(sqrt(pow(GxRed, 2) + pow(GyRed, 2)));
            productGreen = round(sqrt(pow(GxGreen, 2) + pow(GyGreen, 2)));
            productBlue = round(sqrt(pow(GxBlue, 2) + pow(GyBlue, 2)));

            if (productRed > 255)
            {
                productRed = 255;
            }

            if (productGreen > 255)
            {
                productGreen = 255;
            }

            if (productBlue > 255)
            {
                productBlue = 255;
            }

            image[i][j].rgbtRed = productRed;
            image[i][j].rgbtGreen = productGreen;
            image[i][j].rgbtBlue = productBlue;
        }
    }
    return;
}
