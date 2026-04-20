#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int div_sintetica(int arr[], int size){

    for (int i = 0; i < size/2; i++){
        int temp = arr[i];
        arr[i] = arr[size-1-i];
        arr[size-1-i] = temp;
    }

    if (arr[0] <= 0) return -1;

    for (int c = 0; ;c++ ){
        long long acumulado = arr[0];
        int ok = 1;

        for (int i = 1; i< size; i++){
            acumulado = acumulado*c + arr[i];
            if (acumulado < 0){
                ok = 0;
                break;
            }
        }

        if (ok) return c;
    }
}



int main(){

    int t;

    printf("Ingrese el numero de lineas: ");
    scanf("%d", &t);

    if (t < 3 || t > 100){
        perror("Valor invalido");
        exit(-1);
    }

    char temp;
    int tam[t];
    int array[t][30];
    memset(array, 0, sizeof(array));

    for (int i = 0; i < t; i++) {
        printf("Ingrese los elementos del arreglo separados por espacio: ");

        int j = 0;
        while (scanf("%d%c", &array[i][j], &temp) == 2) {
            j++;
            if (temp == '\n') break;
        }
        tam[i] = j;

        if (tam[i] < 4 || tam[i] > 30){
            perror("Tamaño Invalido");
            exit(-1);
        }
    }


    //Aplicar func
    int a[t];

    for(int i = 0; i < t; i++){
        a[i] = div_sintetica(array[i], tam[i]);
    }

    for(int i = 0; i < t; i++){
        if(a[i] == -1){
        printf("No existe n0, ");
        } else{
        printf("%d, ", a[i]);
        }
    }

    return 0;
}
