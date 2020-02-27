#include <iostream>
using namespace std;

class Solution {
public: 
    void swap_with_zero(int* array, int len, int n){
        int i=0;
        int zerop=0;
        int np=0;
        for (i=0;i<len;i++){
            if (array[i]==0){
                zerop=i;
            }
            else
            {
                if (array[i]==n){
                    np=i;
                }
            }
            
        }
        array[np]=0;
        array[zerop]=n;
    }
    void sort(int* array, int len) {
        int i;
        swap_with_zero(array,len,array[0]);
        for (i=1;i<len;i++){
            int j=0;
            bool youXu=true;
            int k;
            for(k=0;k<i;k++){
                if (array[k]>array[k+1]){
                    youXu=false;
                    break;
                }
            }
            if(!youXu ){
                swap_with_zero(array,len,array[i]);
                for(k=i-1;k>=0;k--){
                swap_with_zero(array,len,array[k]);
                }    
            }
        }
         for(i=0;i<len;i++){
            
            cout<<array[i]<<endl;
            
        }
    }
    
};


int main()
{
    Solution s;
    int arr[7]={2,3,4,5,0,1,9};
    s.sort(arr,7);
    return 0;
}

