#include <stdio.h>
#include <stdlib.h>

int merge(int arr[], int p, int q, int r){
    int nl = q-p+1;
    int nr = r-q;
    
    int L[nl];
    for(int i = 0; i < nl; i++){
        L[i] = arr[p+i];
    }

    int R[nr];
    for (int i = 0; i < nr; i++){
        R[i] = arr[q+i+1]; 
    }

    int i = 0;
    int j = 0;
    int k = p;

    int comp = 0;

    while(i < nl && j < nr){
        comp++;
        if (L[i] <= R[j]){
            arr[k] = L[i];
            i += 1;
        } else {
            arr[k] = R[j];
            j += 1;
        }
        k += 1;
    }

    while (i<nl){
        arr[k] = L[i];
        i += 1;
        k += 1;
    }

    while(j<nr){
        arr[k] = R[j];
        j += 1;
        k += 1;
    }
    return comp;
}


int merge_sort(int arr[],int p, int r){

    int comp = 0;

    if (p < r){
        int q = (p+r)/2;
        comp += merge_sort(arr,p,q);
        comp += merge_sort(arr,q+1,r);
        comp += merge(arr,p,q,r);
    }
    return comp;
}


int main() {

    int n;

    printf("Ingrese el tamaño del arreglo: ");
    scanf("%d",&n);

    int arreglo[n];

    for(int i = 0; i < n; i++){
        printf("\nIngrese los elementos del arreglo: ");
        scanf("%d",&arreglo[i]);
    }

    //The array is sorted
    int comp = merge_sort(arreglo, 0, n-1);


    for (int i = 0; i < n; i++) {
        printf("%d ",arreglo[i]);
    }

    printf("\nNumero de comparaciones: %d\n", comp);

    return 0;
}