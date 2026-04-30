#include <stdio.h>
#include <stdlib.h>

int romanToInt(char* s) {
    int n =strlen(s);
    int integer = 0;

    if (n < 1 || n > 15){
        perror("Longitud invalida");
        exit(-1);
    }

    for(int i = 0; i < n; i++){
        char temp = (i>0) ? s[i-1]: 0;

        switch(s[i]){
            case 'M':
                integer += (temp == 'C') ? 800 : 1000;
                break;
            case 'D':
                integer += (temp == 'C') ? 300 : 500;
                break;
            case 'C':
                integer += (temp == 'X') ? 80 : 100; 
                break;
            case 'L':
                integer += (temp == 'X') ? 30 : 50;
                break;
            case 'X':
                integer += (temp == 'I') ? 8 : 10;
                break;
            case 'V':
                integer += (temp == 'I') ? 3 : 5;
                break;
            case 'I':
                integer += 1;
                break;
            default:
                perror("Valor invalido");
                exit(-1);
        }
    }

    if(integer < 1 || integer > 3999){
        perror("Valor fuera del rango aceptado");
        exit(-1);
    }
    return integer;
}