#include <stdio.h>
#include <stdlib.h>

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {

    int* result = malloc(2*sizeof(int));

    for(int i = 0; i < numsSize; i++){
        int j = i+1;
        while( j < numsSize){
            if (nums[i] + nums[j] == target){
                result[0] = i;
                result[1] = j;
                *returnSize = 2;
                return result;
            } 
            j++;
        }
    }
    return NULL;
}
