/* ####################################################################### */
/* This script compares the speed of the computation of a polynomial       */
/* in C in a couple of different ways.                                     */
/*                                                                         */
/* Author: Francesc Alted                                                  */
/* Date: 2013-09-04                                                        */
/* ####################################################################### */


#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <sys/time.h>
#include <time.h>
#include <string.h>

#define N  10*1000*1000

double x[N];
double y[N];

/* Given two timeval stamps, return the difference in seconds */
float getseconds(struct timeval last, struct timeval current) {
  int sec, usec;

  sec = current.tv_sec - last.tv_sec;
  usec = current.tv_usec - last.tv_usec;
  return (float)(((double)sec + usec*1e-6));
}

int main(void) {
  long i;
  double inf = -1;
  double dN = 2./N;
  struct timeval last, current;
  float tspend;

  /* Initialize array */
  for(i=0; i<N; i++) {
    x[i] = inf + i*dN;
  }

  /* Commit the y vector (just to be fair with the Python counterparts) */
  memset(y, 0, sizeof(y));

  /* Perform actual computation */
  printf("Starting computation...\n");
  gettimeofday(&last, NULL);
  #pragma omp parallel for private(i) schedule(static)
  // #pragma omp parallel for private(i) schedule(dynamic)
  for(i=0; i<N; i++) {
    // y[i] = .25*pow(x[i],3.) + .75*pow(x[i],2.) - 1.5*x[i] - 2;  // 0)
    y[i] = ((.25*x[i] + .75)*x[i] - 1.5)*x[i] - 2;               // 1)
    // y[i] = x[i];                                                // 2)
    // y[i] = pow(sin(x[i]), 2.) + pow(cos(x[i]), 2.);             // 3)
  }
  gettimeofday(&current, NULL);
  tspend = getseconds(last, current);
  printf("Compute time:\t %.3f s\n", tspend);

  return(0);
}

