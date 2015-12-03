#include <stdio.h>
#include <aSubRecord.h>
#include <registryFunction.h>
#include <epicsExport.h>
#include <string.h>

static long profile_value_reverse(aSubRecord *precord)
{
    int lx;
    int ly;

    int *x;
    int *y;

    // get dimension of camera image data array
    lx = *(int*) precord->a;
    ly = *(int*) precord->b;

    // get data
    x = (int *) precord->c;
    y = (int *) precord->d;

    // compute reverse arrays
    int i,j;
    int rx[lx];
    int ry[ly];

    for(i=lx-1,j=0;i>=0;i--,j++)
    {   
        rx[j] = x[i];
    }

    for(i=ly-1,j=0;i>=0;i--,j++)
    {
        ry[j] = y[i];
    }

    // send to VALA and VALB
    memcpy(precord->vala,rx,precord->nova*sizeof(int));
    memcpy(precord->valb,ry,precord->novb*sizeof(int));

    return 0;

}

static long profile_index(aSubRecord *precord)
{

    int lx;
    int ly;
    int i;
    int type;

    // get dimension of camera image data array
    lx = *(int*) precord->a;
    ly = *(int*) precord->b;
    type = *(int*)precord->c;

    // init arrays
    int x[lx];
    int y[ly];

    // calculate the array of indexes for the profile in X
    for(i=0;i<lx;i++)
    {
       x[i] = i;
       //printf("-- %ld ",x[i]);
    }
    memcpy(precord->vala,x,precord->nova*sizeof(int));


    // calculate the array of indexes for the profile in Y
    for(i=0;i<ly;i++)
    {
       y[i] = i;
       //printf("== %ld ",y[i]);
    }
    memcpy(precord->valb,y,precord->novb*sizeof(int));


    return 0;
}

static long sign_conversion(aSubRecord *precord)
{
    char *imgIn;

    // get image file path from INPA
    imgIn = (char *) precord->a;

    // save data to VALA
    memcpy(precord->vala, imgIn, precord->nova*sizeof(unsigned char));

    return 0;
}

static long limit_values(aSubRecord *precord)
{
    int i;
    char *imgIn;
    char *imgOut;
    long length;

    // get image file path from INPA
    imgIn = (char *) precord->a;

    imgOut = imgIn;

    length = (long) precord->noa;

    for (i=0; i<length; i++) {
        imgOut[i] = imgIn[i] < 0 ? 127 : imgIn[i];
    }

    // save data to VALA
    memcpy(precord->vala, imgOut, precord->nova*sizeof(unsigned char));

    return 0;
}

static long change_monitoring(aSubRecord *precord)
{
    // get current image counter
    int counter_current = *(int*) precord->a;

    // store current value as previous later for next call
    *(long *) precord->vala = counter_current; 

    // get the previous value
    int counter_old = *(int*) precord->b;

    // output 1 to OUTB is change is detected, 0 otherwise
    *(long *) precord->valb = counter_current > counter_old ? 1 : 0; 
 
    return 0;
}

epicsRegisterFunction(profile_index);
epicsRegisterFunction(profile_value_reverse);
epicsRegisterFunction(sign_conversion);
epicsRegisterFunction(limit_values);
epicsRegisterFunction(change_monitoring);

