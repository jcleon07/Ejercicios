#include <stdio.h>
#include <stdlib.h>
#include <math.h>


//TOP DOWN SOLUTION (EXPONENTIAL TIME)
int recursive_matrix_chain(int *p, int i, int j){

    if (i == j){
        return 0;
    }

    int m_ij = (-INFINITY);

    for (int k = 0; k < j-1; k++) {

        int q = recursive_matrix_chain(p, i, k) 
        + recursive_matrix_chain(p, k+1, j) 
        + (p[i-1]*p[k]*p[j]);

        if (q < m_ij){
            m_ij = q;
        }
    }

    return m_ij;
}