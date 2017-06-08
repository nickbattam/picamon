#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <registryFunction.h>
#include <aSubRecord.h>
#include <menuFtype.h>
#include <errlog.h>
#include <epicsExport.h>
#include <sys/types.h>

const int MAX_STRING_LENGTH = 40;

static long _readlist(char filename[], void *destination)
{
    FILE *fp;

    // open file and make sure it's opened properly
    fp = fopen(filename,"r");
    if(NULL == fp) 
    {
        fprintf(stderr,"cannot open file\n");
        return 1;
    }

    // max line size defined
    size_t buffer_size = 80;
    char *line = malloc(buffer_size * sizeof(char));

    // read each line
    int i=0;
    while(-1 != getline(&line, &buffer_size, fp))
    {

        // getting rid of the trailing '\n'
        if ( '\n' == line[strlen(line) - 1])      
            line[strlen(line) - 1] = 0;

        // copy string to destination record
        memcpy(destination+MAX_STRING_LENGTH*i, line, MAX_STRING_LENGTH*sizeof(char));
        i++;
    }

    fclose(fp);
    free(line);

    return 0;
}

static long readlist(aSubRecord *prec)
{
    long e = 0;
    
    e &= _readlist("camera.list", prec->vala);
    e &= _readlist("monitor.list", prec->valb);

    return e;
}

static long _readcmap(char filename[],void *destination)
{
    FILE *fp;
    int i,j;

    const char DELIMITERS[] = " \t,;-";

    // open file and make sure it's opened properly
    fp = fopen(filename,"r");
    if(NULL == fp) 
    {
        fprintf(stderr,"cannot open file\n");
        return 1;
    }

    // max line size defined
    size_t buffer_size = 80;
    char *line = malloc(buffer_size * sizeof(char));

    // read each line
    j=0;
    while(-1 != getline(&line, &buffer_size, fp))
    {
        char rgb[7];

        // split input line into tokens
        // convert rgb values to hexadecimal string
        char *pch;
        pch = strtok(line, DELIMITERS);
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
    free(line);

    return 0;
}

static long readcmap(aSubRecord *prec)
{
    long e = 0;

    e &= _readcmap("colormaps/gray", prec->vala);
    e &= _readcmap("colormaps/jet", prec->valb);
    e &= _readcmap("colormaps/hot", prec->valc);
    e &= _readcmap("colormaps/coolwarm", prec->vald);
    e &= _readcmap("colormaps/bone", prec->vale);

    return e;
}

epicsRegisterFunction(readcmap);
epicsRegisterFunction(readlist);

