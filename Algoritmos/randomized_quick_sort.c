#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int partition(int A[],int p, int r){
    int x = A[r];
    int i = p-1;

    for(int j = p; j < r; j++){
        if(A[j] <= x){
            i = i+1;
            int temp = A[i];
            A[i] = A[j];
            A[j] = temp;
        }
    }
    int temp2 = A[i+1];
    A[i+1] = A[r];
    A[r] = temp2;

    return i+1;
}

int quickSort(int A[],int p,int r){
    if (p < r){
        int q = partition(A,p,r);
        quickSort(A,p,q-1);
        quickSort(A,q+1,r);
    }
    return 0;
}



/*          RANDOMIZED FUNCTIONS        */

int randomized_partition(int A[],int p, int r){
    int i = rand() % (r-p+1) + p;
    int temp = A[r];
    A[r] = A[i];
    A[i] = temp; 
    return partition(A,p,r);
}


int randomized_quicksort(int A[], int p, int r){

    if (p < r){
        int q = randomized_partition(A,p,r);
        randomized_quicksort(A,p,q-1);
        randomized_quicksort(A,q+1,r);
    }   
    
    return 0;
}



int main() {

    srand(time(NULL));

    int A[] = {4,896,2,7,92,5,7,59,7,82};

    int n = sizeof(A) / sizeof(A[0]);
    randomized_quicksort(A, 0, n - 1);

    for(int i = 0; i < n; i++){
        printf("%d ", A[i]);
    }

    return 0;
}