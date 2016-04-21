#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <registryFunction.h>
#include <aSubRecord.h>
#include <menuFtype.h>
#include <errlog.h>
#include <epicsExport.h>
#include <sys/types.h>

static long _readcmap(char filename[],void *destination)
{
    FILE *fp;
    int i,j;

    const char DELIMITERS[] = " \t,;-";
    const int MAX_STRING_LENGTH = 40;

    // open file and make sure it's opened properly
    fp = fopen(filename,"r");
    if(NULL == fp) 
    {
        fprintf(stderr,"cannot open file\n");
        return 1;
    }

    // max line size defined
    size_t buffer_size = 80;
    char *buffer = malloc(buffer_size * sizeof(char));

    // read each line
    j=0;
    while(-1 != getline(&buffer, &buffer_size, fp))
    {
        char rgb[7];

        // split input line into tokens
        // convert rgb values to hexadecimal string
        char *pch;
        pch = strtok(buffer, DELIMITERS);
        i=0;
        while(pch != NULL)
        {          
            sprintf(&rgb[i], "%02x", atoi(pch));
            pch = strtok(NULL, DELIMITERS);
            i = i+2;
        }
   
        // copy hexadecimal string into record output VALA
        memcpy(destination+MAX_STRING_LENGTH*j, rgb, MAX_STRING_LENGTH*sizeof(char));
        j++;

    }

    fclose(fp);
    free(buffer);

    return 0;
}

static long readcmap(aSubRecord *prec)
{

    _readcmap("colormaps/gray",prec->vala);
    _readcmap("colormaps/jet",prec->valb);
    _readcmap("colormaps/hot",prec->valc);
    _readcmap("colormaps/coolwarm",prec->vald);
    _readcmap("colormaps/bone",prec->vale);

    return 0;
}

epicsRegisterFunction(readcmap);

