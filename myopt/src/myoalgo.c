#include <stdio.h>
#include <stdlib.h>
#include "myopt.h"

int myofind_feasible(myo *pmyo);
int myo_iteration(myo *pmyo);
int myo_getgradient(myo *pmyo);
int myo_step(myo *pmyo);
void myo_showx(myo *pmyo, int start, int end);
void myoVtimesy(myo *pmyo, double *y);
int myoprepare(myo *pmyo);
// custom headers
int descending_compare_quicksort_func(const gradient_type* a, const gradient_type* b);

#define LOUDFEASIBLE

int myoalgo(myo *pmyo)
{
  int retcode = 0;
  int max_its = 2;

  if((retcode = myoprepare(pmyo))) goto BACK;

  if((retcode = myofind_feasible(pmyo))) goto BACK;

  for(pmyo->iteration = 0; pmyo->iteration < max_its; pmyo->iteration++){
    if((retcode = myo_iteration(pmyo))) goto BACK;
    myo_showx(pmyo, 0, pmyo->n-1);
  }

 BACK:
  printf("myoalgo returning with code %d\n\n", retcode);
  return retcode;
}
int myoprepare(myo *pmyo)
{
  int retcode = 0;
  int i, j, k, f = pmyo->f, n = pmyo->n;
  double sum, *V = pmyo->V, *F = pmyo->F;
  /** first compute VtF, which is an nxf matrix **/

  for(j = 0; j < n; j++){
    for(i = 0; i < f; i++){
      /* compute the (j,i) entry of VtF */
      sum = 0;
      for (k = 0; k < f; k++){
	sum  += V[k*n + j]*F[k*f + i];
      }
      pmyo->VtF[j*f + i] = sum;
    }
  }
  printf("myoprepare returns %d\n", retcode);
  return retcode;
}
  
int myofind_feasible(myo *pmyo)
{
  int retcode = 0;
  int j;
  double sum, *x = pmyo->x, delta;

  sum = 0;
  for(j = 0; j < pmyo->n; j++){
    x[j] = pmyo->lower[j];  /** we assume lower <= upper, but should
				      check **/
#ifdef LOUDFEASIBLE
    printf("  -> x[%d] initialized at %g\n", j, x[j]);
#endif

    sum += x[j];
  }
  if(sum > 1.0){
    printf(" error: sum of asset lower bounds equals %g > 1.0\n", sum);
    retcode = DATAERROR1; goto BACK;
  }

  for(j = 0; (j < pmyo->n) && (sum < 1.0) ; j++){
    if(sum < 1.0){
      delta = (1.0 - sum < pmyo->upper[j] - pmyo->lower[j]) ?
	1.0 - sum : pmyo->upper[j] - pmyo->lower[j];
      sum += delta;
      x[j] += delta;
    }
#ifdef LOUDFEASIBLE
    printf("  -> x[%d] increased to %g\n", j,x[j]);
#endif
  }
  printf("find_feasible done at j = %d\n", j);

 BACK:
  return retcode;
}

int myo_iteration(myo *pmyo)
{
  int retcode = 0;

  printf("\niteration %d\n", pmyo->iteration);

  if( (retcode = myo_step(pmyo))) goto BACK;

 BACK:
  return retcode;
}

int myo_getgradient(myo *pmyo)
{
  int retcode = 0, i, j, n = pmyo->n, f = pmyo->f;
  double *Vx = pmyo->Vx, *VtF = pmyo->VtF, sum;

  printf(" computing gradient at iteration %d\n", pmyo->iteration);
  myoVtimesy(pmyo, pmyo->x);
  for(j = 0; j < n; j++){
    /** first initialize the gradient **/

    pmyo->gradient[j] = -pmyo->mu[j] + 2*pmyo->sigma2[j]*pmyo->x[j];

    /** computes jth entry of VtFVx */
    sum = 0;
    for(i = 0; i < f; i++){
      sum += VtF[j*f + i]*Vx[i];
    }
    pmyo->gradient[j] += 2*sum;
  }

  return retcode;
}


int myo_step(myo *pmyo)
{
  int retcode = 0;
  // struct fields
  int n = pmyo->n;
  int f = pmyo->f;
  double* x = pmyo->x;
  double* gradient = pmyo->gradient; 
  double* upper = pmyo->upper;
  double* lower = pmyo->lower;
  double* y = pmyo->y;
  gradient_type* gradients = pmyo->gradients;
  double* descending_y = pmyo->descending_y;
  double* descending_optimized_y = pmyo->descending_optimized_y;
  printf(" computing step at iteration %d\n", pmyo->iteration);

  if( (retcode = myo_getgradient(pmyo))) goto BACK;

  /** next, sort gradient **/
  printf("************ORIGINAL GRADIENT**********\n");
  for(int i = 0; i < pmyo->n; i++){
    printf("%g ", pmyo->gradient[i]);
  }
  printf("\n************ORIGINAL GRADIENT END**********");

  // copy gradient into gradients along with their index
  for (int i = 0; i < pmyo->n; i++) {
    gradients[i].idx = i;
    gradients[i].value = pmyo->gradient[i];
  }


  // qsort((void*)gradients, pmyo->n, sizeof(gradient), (int(*)(const void*,const void*))descending_compare_quicksort_func);
  qsort((void*)gradients, pmyo->n, sizeof(gradient_type), (int(*)(const void*,const void*))descending_compare_quicksort_func);
  printf("************SORTED GRADIENT**********\n");
  
  for(int i = 0; i < pmyo->n; i++){
    printf("{idx: %d, value: %g} ", gradients[i].idx, gradients[i].value);
  }
  printf("\n************SORTED GRADIENT END**********");


  /** next, compute direction **/
  double optimal_cost = 0.0;
  int feasible_y_count = 0;
  for (int k = 0; k < n; k++) {

    double total = 0;
    for (int j = 0; j < k; j++) {
      descending_y[j] = lower[gradients[j].idx] - x[gradients[j].idx];
      total += descending_y[j];
    }
    for (int j = k + 1; j < n; j++) {
      descending_y[j] = upper[gradients[j].idx] - x[gradients[j].idx];
      total += descending_y[j];
    }
    printf("\ntotal: %g", total);
    descending_y[k] = -total;
    int is_y_feasible = 1;
    
    // feasible iff lj ≤ x(k) + y(k) ≤ uj for all j
    for(int j = 0; j < n; j++) {
      int idx = gradients[j].idx;
      if(lower[idx] <= (x[idx] + descending_y[j]) && (x[idx] + descending_y[j]) <= upper[idx]) {
        
      } else {
        is_y_feasible = 0;
        break;
      }
    }

    if(is_y_feasible) {
      double cost = 0.0;
      for(int j = 0; j < n; j++) {

        cost += gradients[j].value * descending_y[j];
      }

      // every time the optimal cost is reset to the newest
      // lower cost until it is impossible to find a lower one
      // when feasible_y_count is <= 0
      if(feasible_y_count <= 0 || cost < optimal_cost) {
        feasible_y_count+=1;
        // find the optimal cost and set it to the variable if the current cost is lower
        optimal_cost = cost;
        for(int j = 0; j < n; j++) {
          descending_optimized_y[j] = descending_y[j];
        }
      }
      
    }

  }

  
  if(feasible_y_count > 0) {
    printf("\nfeasible_y_count: %d\n", feasible_y_count);
  } else {
    printf("unfeasible y; exiting\n");
    return 1;
  }

  printf("\nMost Optimal Cost: %g\n", optimal_cost);
  // set y to the optimized y's using the original index
  for(int i = 0; i < n; i++) {
    y[gradients[i].idx] = descending_optimized_y[i];
  }
  for(int i = 0; i < n; i++) {
    printf("new y: %g\n", y[i]);
  }

  /** next, compute step size **/
 BACK:
  return retcode;
}

void myoVtimesy(myo *pmyo, double *y)
{
  /** here y is an n-vector, and we compute V*y and place it in pmyo->Vx **/
  int i, j, f = pmyo->f, n = pmyo->n;
  double sum, *V = pmyo->V;

  for(i = 0; i < f; i++){
    sum = 0;
    for(j = 0; j < n; j++){
      sum += V[i*n + j]*y[j];
    }
    pmyo->Vx[i] = sum;
  }
}

void myo_showx(myo *pmyo, int start, int end)
{
  int j;

  start = start < 0 ? 0 : start;
  end = end >= pmyo->n ? pmyo->n-1 : end;
  printf("\n");
  for(j = start; j <= end; j++){
    printf("  x[%d] = %g\n", j, pmyo->x[j]);
  }
  printf("\n");
}

int descending_compare_quicksort_func(const gradient_type *a,const gradient_type *b) {
  // if ((double *) a > (double *) b) {
  //   return -1;
  // } else if((double *) a < (double *) b) {
  //   return 1;
  // } else {
  //   return 0;
  // }

  if (a->value < b->value) return 1;
  else if (a->value > b->value) return -1; return 0;


}
