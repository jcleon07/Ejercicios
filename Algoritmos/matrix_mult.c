#include <stdio.h>
#include <stdlib.h>

int** matrix_multiply(int **a, int **b){

    int a_cols = sizeof(a) / sizeof(a[0]);
    int a_rows = sizeof(a[0]) / sizeof(a[0][0]);
    int b_cols = sizeof(b) / sizeof(b[0]);
    int b_rows = sizeof(b[0]) / sizeof(b[0][0]);

    if (a_cols != b_rows){
        perror("Incompatible dimensions");
        exit(-1);
    } else {
        int **c = (int**)malloc(a_cols*sizeof(int*));

        for (int i = 0; i < a_rows; i++){
            c[i] = (int*)malloc(b_cols*sizeof(int));

            for (int j = 0; j < b_cols; j++){
                c[i][j] = 0;

                for(int k = 1; k < a_cols; i++){
                    c[i][j] = c[i][j] + a[i][k]*b[k][j];
                }
            }
        }
        return c;
    }
}

