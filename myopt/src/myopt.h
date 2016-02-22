#ifndef MYO

#define MYO


typedef struct gradient {
  int idx;
  double value;
} gradient;


typedef struct myo{
  int n;
  int f;
  int iteration;
  double *mu;
  double *sigma2;
  double *V;
  double *upper;
  double *lower;
  double *F;
  double *gradient;
  double *x;
  double *Vx;
  double *VtF;

  // custom struct fields
  gradient *gradients;
}myo;

#define NOMEM 100
#define DATAERROR1 101
 
int myoGetmyoFromFile(myo **ppmyo, char *filename);
int myocreatemyo(myo **pmyo);
void myokillmyo(myo **ppmyo);
int myoalgo(myo *pmyo);

#include "utilities.h"

#endif
