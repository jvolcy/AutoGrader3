// HWC1014
// Using the array, place the input height in the correct
// spot in the graduation line array.
#include <iostream>
using namespace std;

//define function inHeight
float inHeight(float x, const int NUM_STUDENTS, float heights[NUM_STUDNETS], float heights) {
    //define int's
    float low = 0;
    float mid;
    float high = NUM_STUDENTS - 1;
    
    //start while loop
    while(high - low != 1)
    {
        mid = (high + low)/2;
        float newMid = heights[mid];
        
        //define if statements
        if ( x > newMid){
            mid = low;
            high = high;
        }
        else if ( x < newMid){
            low = low;
            mid = high;
        }
        else if ( x == newMid){
            low = mid;
            high = mid++;
        }
        
        cout <<"Your height is between "<< low <<"and "<<high<<endl;
}
    
//define main function
int main()
{
    const int NUM_STUDENTS = 50;
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
        
    //get input
    float x;
    cout <<"enter your height: "<< endl;
    cin >> x;
        
    //call le function
    inHeight(x, NUM_STUDENTS, heights[NUM_STUDNETS]);
    
    //print where the new height would go in between
    
        
    return 0;
}
