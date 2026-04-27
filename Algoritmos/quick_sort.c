#include <stdio.h>
#include <stdlib.h>

int partition(int A[],int p, int r){
    int x = A[r];
    int i = p-1;

    for(int j = p; j < r-1; j++){
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


int main (){
    
    int A[] = {2,7,4,2,8,4,5}; 
    
    quickSort(A,0,6);
    
    for(int i = 0; i<6; i++){
        printf("%d ",A[i]);
    }
    
    return 0;
}