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

    char delimiters[] = " \t,;-";

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
        pch = strtok(buffer, delimiters);
        i=0;
        while(pch != NULL)
        {          
            sprintf(&rgb[i], "%02x", atoi(pch));
            pch = strtok(NULL, delimiters);
            i = i+2;
        }
   
        // copy hexadecimal string into record output VALA
        memcpy(destination+40*j,rgb,40*sizeof(char));
        j++;

    }

    fclose(fp);
    free(buffer);

    return 0;
}

static long readcmap(aSubRecord *prec)
{
    _readcmap("gray",prec->vala);
    _readcmap("jet",prec->valb);
    _readcmap("hot",prec->valc);
    _readcmap("coolwarm",prec->vald);
    _readcmap("bone",prec->vale);

    return 0;
}

epicsRegisterFunction(readcmap);

