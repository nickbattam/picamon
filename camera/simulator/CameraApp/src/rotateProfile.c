#include <stdio.h>
#include <aSubRecord.h>
#include <registryFunction.h>
#include <epicsExport.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

static int rotate_crosshair(aSubRecord *precord){
    float *a, *b, *c, *d, *e, *f, *g, *h, *outa, *outb, *outc, *outd, *oute;
    
    //Inputs
    a = (float *)precord->a;       //Input A - Type
    b = (float *)precord->b;       //Input B - Current
    c = (float *)precord->c;       //Input C - X
    d = (float *)precord->d;       //Input D - Y
    e = (float *)precord->e;       //Input E - MAX_X
    f = (float *)precord->f;       //Input F - MAX_Y
    g = (float *)precord->g;
    h = (float *)precord->h;
    //Outputs
    outa = (float *)precord->vala; //Output A - X
    outb = (float *)precord->valb; //Output B - Y
    outc = (float *)precord->valc; //Output C - Current
    outd = (float *)precord->vald;
    oute = (float *)precord->vale;
    int type = (int)a[0];
    int current_type = (int)b[0];
    int old_x = (int)c[0];
    int old_y = (int)d[0];
    int max_x = (int)e[0];
    int max_y = (int)f[0];
    int old_soft_x = (int)g[0];
    int old_soft_y = (int)h[0];
    if (type != current_type){
        switch(type){
            case 0:
                switch(current_type){
                    case 1:
                        outa[0]=max_x - old_y;
                        outb[0]=old_x;
                        outd[0]=max_x - old_soft_y;
                        oute[0]=old_soft_x;
                        break;
                    case 2:
                        outa[0]=old_y;
                        outb[0]=max_y - old_x;
                        outd[0]=old_soft_y;
                        oute[0]=max_y - old_soft_x;
                        break;
                }
                break;
            case 1:
                switch(current_type){
                    case 0:
                        outa[0]=old_y;
                        outb[0]=max_x - old_x;
                        outd[0]=old_soft_y;
                        oute[0]=max_x - old_soft_x;
                        break;
                    case 2:
                        outa[0]=max_y - old_x;
                        outb[0]=max_x - old_y;
                        outd[0]=max_y - old_soft_x;
                        oute[0]=max_x - old_soft_y;
                        break;
                }
                break;
            case 2:
                switch(current_type){
                    case 0:
                        outa[0]=max_y - old_y;
                        outb[0]=old_x;
                        outd[0]=max_y - old_soft_y;
                        oute[0]=old_soft_x;
                        break;
                    case 1:
                        outa[0]=max_y - old_x;
                        outb[0]=max_x - old_y;
                        outd[0]=max_y - old_soft_x;
                        oute[0]=max_x - old_soft_y;
                        break;
                }
                break;
        }
    }
    else{
        outa[0] = old_x;
        outb[0] = old_y;
        outd[0] = old_soft_x;
        oute[0] = old_soft_y;
    }
    outc[0] = type;
    return 0;
}

epicsRegisterFunction(rotate_crosshair);
