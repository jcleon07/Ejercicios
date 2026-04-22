#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

char* master_method(char func[]){

    int k = 0;
    int n = strlen(func);
    int nums[4] = {0};
    char* out = malloc(100);        

    for(int i = 0; i < n; i++){
        if(isdigit(func[i]) || func[i] == '-'){
            int number = 0;
            int sign = 1;

            if(func[i] == '-') {
                sign = -1;
                i++;
            }

            while(i < n && (isdigit(func[i]) || func[i] == '-')){
                number = number*10 + (func[i] - '0');
                i++; 
            }
            nums[k++] = sign * number;
            i--;  
            } 
        }
    
        if (nums[0] < 1 || nums[1] <= 1|| nums[2] <= 0 || nums[3] < 0 ){
            perror("ERROR: Valor invalido\n");
            exit(-1);
        }

        printf("DEBUG: Array de nums: ");

        for (int i = 0; i < 4; i++){
            printf("%d ", nums[i]);
        }

    if (nums[0] <= (int)pow(nums[1],nums[3])){
        if(nums[3] == 0){
            snprintf(out, 100, "O(");      
        } else if(nums[3] == 1) {
            snprintf(out, 100, "O(n" );
        } else {
            snprintf(out, 100, "O(n^(%d)", nums[3]);  //O(n^d)
        }

        if(nums[0] == (int)pow(nums[1],nums[3])){
            strcat(out, "lg(n)");    //O(nlg(n))
        }

    } else {
        double logar = log(nums[0])/log(nums[1]);
        if (logar == floor(logar)) {
            if (log(nums[0])/log(nums[1]) == 1){
                snprintf(out, 100, "O(n");
            } else {
                snprintf(out, 100, "O(n^(%d))", (int)(log(nums[0])/log(nums[1])));
            }
        } else {
        if (nums[1] == 2){
            snprintf(out, 100, "O(n^(lg(%d))", nums[0]); //O(n^(log_(b)(a)))
        } else {
            snprintf(out, 100, "O(n^(log_(%d)(%d))", nums[1], nums[0]);  //0(n^(lg(a)))
        }
        }
    }  
   
    strcat(out, ")");
    return out;
}



int main() {

    char func[100];

    printf("Inserte la funcion a comparar: ");
    fgets(func, 100, stdin);   //Sin & porque el primer elemento del arreglo sirve como puntero
    //func[strcspn(func, "\n")] = '\0';

    char* res = master_method(func);

    printf("\nEl resultado es: %s", res);

    return 0;
}