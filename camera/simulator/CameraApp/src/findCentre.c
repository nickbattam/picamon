#include <stdio.h>
#include <aSubRecord.h>
#include <registryFunction.h>
#include <epicsExport.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <opencv/highgui.h>
#include <opencv/cv.h>


float calculate_distance(float x1, float y1, float x2, float y2)
{  
    float diffx = x1 - x2;
    float diffy = y1 - y2;
    float diffx_sqr = pow(diffx,2);
    float diffy_sqr = pow(diffy,2);
    float distance = sqrt(diffx_sqr + diffy_sqr);
    return distance;
}

void centre_of_grav(int x, int y, int total, float *cofg){
    cofg[0] = (float)x / (float)total;
    cofg[1] = (float)y / (float)total;
}

CvBox2D find_min_rectangle(CvSeq* contours, double* max_area, int w, int h){
    int area = w * h;
    double temp;
    CvBox2D rect;
    CvMemStorage* storage2 = cvCreateMemStorage(0);

    for (; contours != 0; contours = contours->h_next){
        temp = cvContourArea(contours,CV_WHOLE_SEQ,0);
        if (temp > *max_area){
            if (temp < (0.8*area)){
                *max_area = temp;
                rect = cvMinAreaRect2(contours,storage2);
            }
        }
    }
    return rect;
}

int rectangle_validate(float *cofg, float* boundary, float rect_percent,
                       int w, int h, IplImage* image){

    CvSize size;
    size.height = h;
    size.width = w;

    //Smooth image and threshold using process image value
    IplImage* temp_img = cvCreateImage(size, IPL_DEPTH_8U, 1);
    cvSmooth(image, temp_img, CV_GAUSSIAN, 5,5,5,5);
    cvThreshold(temp_img,temp_img,(int)*boundary,255,CV_THRESH_BINARY);
    CvMemStorage* storage = cvCreateMemStorage(0);
    CvSeq *contours = 0;
    
    //Find Contours of thresholded image
    cvFindContours(temp_img,storage,&contours,sizeof(CvContour),
                   CV_RETR_CCOMP, CV_CHAIN_APPROX_NONE, cvPoint(0,0));
    CvBox2D rect;
    CvPoint2D32f centre;
    double max_area = 0;

    //Find min area rectangle of largest countour
    rect = find_min_rectangle(contours, &max_area, w,h);
    centre = rect.center;
    CvSize2D32f boxco = rect.size;
    double rectsize = boxco.width * boxco.height;

    //If there is a rectangle, and the contour makes up rect_percent% of it
    if ((rectsize > 1)&&((max_area / rectsize)>rect_percent)){
	cofg[0]=centre.x;
	cofg[1]=centre.y;
        return 0;
    }
    return 1;
}

void average_cofg(float *cofg, float *c_of_gx, float *c_of_gy, 
                  int c_of_g_held){
    int i;
    float sum_x = 0, sum_y = 0;
    for(i = 0; i < c_of_g_held; i++){
        sum_x = sum_x + c_of_gx[i];
        sum_y = sum_y + c_of_gy[i];
    }
    cofg[0] = sum_x / c_of_g_held;
    cofg[1] = sum_y / c_of_g_held;
}

int validate_cofg(float fract_above_thresh, float *thresh, int total_x,
                   int total_y, int pixels_above_thresh,  float *c_of_gx,
                   float *c_of_gy, int cog_dist, float thresh_inc,
                   float min_fract, float max_fract, float* boundary, int w,
	           int h, IplImage* image, float *cofg, int method, 
                   int *c_of_g_held, int successive, float rect_percent,
                   int *failure, int* error){
    int not_found = 1;
    if ((min_fract <= fract_above_thresh)&&(max_fract >= fract_above_thresh)){
        centre_of_grav(total_x, total_y, pixels_above_thresh, cofg);
        
        if (*c_of_g_held != 0){
            if (calculate_distance(cofg[0],cofg[1],c_of_gx[*c_of_g_held-1], 
                                   c_of_gy[*c_of_g_held-1]) < cog_dist){
                c_of_gx[*c_of_g_held] = cofg[0];
                c_of_gy[*c_of_g_held] = cofg[1];
                *c_of_g_held = *c_of_g_held + 1;
                if((*c_of_g_held) == successive){
                    not_found = 0;
                }
            }
            else{
                *c_of_g_held = 0;
            }
        }
        else{
            if (successive == 1){
                not_found = 0;
            }
            else{
                c_of_gx[0] = cofg[0];
                c_of_gy[0] = cofg[1];
                *c_of_g_held = 1;
                *error = 4;
            }
        }
        if(!not_found){
            //Return midpoint of rectangle, or average of array
            if(method == 1){
                not_found = rectangle_validate(cofg, boundary, rect_percent, w,
                                               h, image);
                if(not_found){
                    *c_of_g_held = 0;
                    *error = 3;    
                }
            }
            else if (*c_of_g_held > 1){
                average_cofg(cofg, c_of_gx, c_of_gy, *c_of_g_held);
            }
        }
    }
    else{
        if (fract_above_thresh < min_fract){
            *failure = 1;
            if ((*error != 3)&&(*error != 4)){
		*error = 2;
	    }
            return not_found;
        }
        *c_of_g_held = 0;
    }
    if (not_found){
        *thresh = *thresh + thresh_inc;
    }
    return not_found;
}

int process_image(float* thresh, float thresh_inc, float min_fract,
                   float max_fract, int successive, int cog_dist,
                   int w, int h, IplImage* image, float* cofg, int method,
                   float rect_percent, float* boundary, int* error){
    int failure = 0;
    int i,j,temp,total_x,total_y,pixel;
    int min = 255;
    int max = 0; 
    int total_pixels = h * w;
    int c_of_g_held = 0;
    int not_found = 1;
    float fract_above_thresh, pixels_above_thresh;
    float *c_of_gx = malloc(successive * sizeof(float));
    float *c_of_gy = malloc(successive * sizeof(float));
    //Work out maximum and minimum
    for(i = 0; i < h; i++){
        for (j = 0; j < w; j++){
            temp = CV_IMAGE_ELEM(image,uchar,i,j);
            if (temp < min){
                min = temp;
            }
            if (temp > max){
                max = temp;
            }
        }
    }
    //Main thresholding loop
    while ((not_found)&&(0.0 <= *thresh)&&(*thresh < 1)){
        *boundary = min + ((max-min)*(*thresh));
        pixels_above_thresh = 0;
        total_x = 0;
        total_y = 0;
        for (i = 0; i < h; i++){
            for (j = 0; j < w; j++){
                pixel = CV_IMAGE_ELEM(image, uchar, i, j);
                if (pixel >= *boundary){
                    pixels_above_thresh++;
                    total_x = total_x + j;
                    total_y = total_y + i;
                }
            }
        }
        fract_above_thresh = pixels_above_thresh / total_pixels;
        not_found = validate_cofg(fract_above_thresh, thresh, total_x, 
                                  total_y, pixels_above_thresh, c_of_gx, 
                                  c_of_gy, cog_dist, thresh_inc,  min_fract, 
                                  max_fract, boundary, w, h, image, cofg, 
                                  method, &c_of_g_held, successive, 
                                  rect_percent, &failure, error);
        if (failure == 1){
	    free(c_of_gy); free(c_of_gx);
            return not_found;
        }
    }
    if (not_found){
        *error = 1;
    }
    free(c_of_gy); free(c_of_gx);
    return not_found;
} 

int controller(uchar* b, float* cofg, int w, int h, int method, 
                int new_width, int new_height, float *thresh, float thresh_inc,
                float min_fract, float max_fract, int successive, 
                int cog_dist, float rect_percent, float* boundary, int* error){
    CvSize size;
    int success = 0;
    CvScalar sca;
    size.height = h; size.width = w;
    IplImage* img2 = cvCreateImage(size, IPL_DEPTH_8U, 1);
    int i, j;
    for(i = 0; i < h; i++){
        for(j = 0; j < w; j++){
            sca.val[0] = b[(i*w) + j];
            cvSet2D(img2,i,j,sca);
        }
    }
    IplImage* img = cvCreateImage(cvSize(new_width, new_height),
                                  IPL_DEPTH_8U,1);
        cvResize(img2, img, CV_INTER_LINEAR);
        cvReleaseImage(&img2);
        success = (!process_image(thresh,thresh_inc,min_fract,max_fract,
                                successive,cog_dist,new_width,new_height,
                                img,cofg,method,rect_percent, boundary, error));
    cvReleaseImage(&img);
    return success;
}

static int find_centre(aSubRecord *precord){
    clock_t begin, end;
    double time_spent;
    begin = clock();
    uchar *a;
    float *b, *c, *d, *e, *f, *g, *h, *i, *j, *k, *l, *m, *n, *o, *outa, *outb, *outc;
    float *outd, *oute, *outf; //Used to check if centroid found

    //Inputs
    a = (uchar *)precord->a;      //Input A - Image
    b = (float *)precord->b;       //Input B - Width
    c = (float *)precord->c;       //Input C - Height
    d = (float *)precord->d;       //Input D - Method
    e = (float *)precord->e;       //Input E - DownsampleX
    f = (float *)precord->f;       //Input F - DownsampleY
    g = (float *)precord->g;       //Input G - Threshold
    h = (float *)precord->h;       //Input H - Thresh Inc
    i = (float *)precord->i;       //Input I - Max Fract
    j = (float *)precord->j;       //Input J - Min Fract
    k = (float *)precord->k;       //Input K - Successive
    l = (float *)precord->l;       //Input L - Cog Dist
    m = (float *)precord->m;       //Input M - Rectangle Percentage
    n = (float *)precord->n;       //Input N - Which algorithm is in use
    o = (float *)precord->o;       //Input O - Is the camera streaming?

    //Outputs
    outa = (float *)precord->vala; //Output A - COFG_X
    outb = (float *)precord->valb; //Output B - COFG_Y
    outc = (float *)precord->valc; //Output C - Time Elapsed
    outd = (float *)precord->vald; //Output D - Whether COFG found
    oute = (float *)precord->vale; //Output E - Which error occurred
    outf = (float *)precord->valf; //Output F - Final Threshold

    //Check if this algorithm is being used
    if ((n[0] != 1)||(o[0] != 1)){
        end = clock();
        time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
        outc[0] = time_spent;
        return 0;
    }

    int error = 0;
    int method = (int)d[0];
    int downsample_w = (int)e[0];
    int downsample_h = (int)f[0];
    float thresh = g[0] / 100;
    float thresh_inc = h[0] / 100;
    float max_fract = i[0] / 100;
    float min_fract = j[0] / 100;
    if(min_fract > max_fract){
        return 0;
    }
    int width = b[0];
    int height = c[0];
    int successive = k[0];
    int cog_dist = l[0];
    float rect_percent = m[0]/100;
    float boundary;
    if ((height != 0)&&(width != 0)){
        float cofg[2];
        if((downsample_w == 0)||(downsample_h == 0)
            ||(downsample_w > width)||(downsample_h > height)){
            downsample_w = width;
            downsample_h = height;
        }
        if(controller(a, cofg, width, height, method, downsample_w, 
                      downsample_h, &thresh, thresh_inc, min_fract, 
                      max_fract, successive, cog_dist, rect_percent, &boundary, 
                      &error)){
            outa[0] = cofg[0] * (width/(float)downsample_w);
            outb[0] = cofg[1] * (height/(float)downsample_h);
            outd[0] = 1;
        }
        else{
            outa[0] = 0;
            outb[0] = 0;
            outd[0] = 0;
            oute[0] = error;
        }
	outf[0] = boundary;
        end = clock();
        time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
        outc[0] = time_spent;
    }
    return 0;
}

epicsRegisterFunction(find_centre);
