#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

//define what a BYTE is
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //check for arguments
    if (argc != 2)
    {
        printf("Usage: ./recover infile\n");
        return 1;
    }

    // open raw input file
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    //set outfile pointer to NULL
    FILE *outptr = NULL;

    //create an array of 512 bytes to store 512 bytes from the raw file at a time
    BYTE buffer[512];

    int jpeg = 0;

    //string to hold a filename
    char filename[8] = "        ";

    //read raw file until the end of file
    while (fread(buffer, sizeof(buffer), 1, inptr) == 1)
    {
        //check if jpeg is found
        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3] & 0xF0) == 0xE0)
        {
            //close outptr if jpeg was found before and written into ###.jpg
            if (outptr != NULL)
            {
                fclose(outptr);
            }

            //setup the filename
            sprintf(filename, "%03d.jpg", jpeg++);

            //open a new outptr for writing a new found jpeg
            outptr = fopen(filename, "w");
        }

        //keep writing to jpeg file if new jpeg is not found
        if (outptr != NULL)
        {
            fwrite(buffer, sizeof(buffer), 1, outptr);
        }
    }

    if (outptr != NULL)
    {
        fclose(outptr);
    }

    //close input file
    fclose(inptr);

    return 0;
}