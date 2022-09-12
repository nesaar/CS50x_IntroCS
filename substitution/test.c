#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main ()
{
      char B[] = "DWUSXNPQKEGCZAJBTLYROHIAVM";
      printf ("String is \"%s\"\n", B);
      for (int i = 0, h = strlen(B); i < h; i++)
      {
            int count = 1;
            for (int j = i + 1; B[j] != '\0'; j++)
            {
                  if (B[i] == B[j])
                  {
                         count++;
                         B[j] = -1;
                  }
            }
            if (count > 1 && B[i] != -1)
           {
                 printf ("\'%c\' is appearing: %d times\n", B[i], count);
           }
      }
      return 0;
}