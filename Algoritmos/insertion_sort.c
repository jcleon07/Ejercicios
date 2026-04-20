#include <stdio.h>
#include <stdlib.h>


int insertion_sort(int arr[],int n) {

    int comp = 0;

    for (int i = 1; i <= n-1; i++){
        int key = arr[i];
        int j = i-1;

        while (j > -1){
            comp++;

            if(arr[j] > key) {
                arr[j+1] = arr[j];
                j = j-1;
            } else {
                break;
            }
        }
        
        arr[j+1] = key;        
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
    int comp = insertion_sort(arreglo,n);

    //We print the sorted array
    for (int i = 0; i < n; i++) {
        printf("%d ",arreglo[i]);
    }

    //We print the number of comparisons
    printf("\nNumero de comparaciones: %d\n",comp);

    return 0;
}