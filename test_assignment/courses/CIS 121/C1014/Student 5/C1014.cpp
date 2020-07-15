/*
Graduation Lineup
C1014.cpp
*/

#include <iostream>
#include <string>
using namespace std;

void findPosition(int size, float heights[], double spelmanite){
    
    //make hi, lo, and mid;
    int hi = size - 1;
    int lo = 0;
    int mid;
    
    //while the hi element and lo element are not next to each other
    while ((hi - lo) != 1){
        
        //get the average value to find the middle 
        mid = (hi + lo)/2;
        
        
        /*if the spelmanites height is less than the value found in the array by placing mid value for index
        then keep the lo at 0 and set the new hi value to the mid value that was just found*/
        if (spelmanite < heights[mid]){
            lo = 0;
            hi = mid;
        }
        
         /*if the spelmanites height is greater than the value found in the array by placing mid value for index
        then keep the hi at the value it already was and set the new lo value to the mid value that was just found*/
        if (spelmanite > heights[mid]){
            lo =  mid;
            hi = hi;
        }
        
         /*if the spelmanites height is the same as the value found in the array by placing mid value for index
        then set the lo to the mid just found and set the hi value to the mid plus one so that
        the spelmanites height is placed next to the duplicate value*/
        if (spelmanite == heights[mid]){
            
            lo = mid;
            hi = mid + 1;
            
        }
        
        
    }
    /*if there is a case that the spelmanite is shorter than the first element in the array
    then let the Spelmanite know that they need to be in the front of the line*/
    if (spelmanite < heights[0]){
        cout << "This Spelmanite needs to be in the front of the line"<< endl;  
    }
    
    /*if there is a case that the spelmanite is taller than the last element in the array
    then let the Spelmanite know that they need to be in the back of the line*/
    else if (spelmanite > heights[hi]){
        cout << "This Spelmanite needs to be in the back of the line" << endl;
    }
    
    //let the spelmanite know where they should be in the line
    else{
        cout<< "This Spelmanite needs to be between Spelmanite " << lo + 1 << " and Spelmanite " << hi + 1<< "." << endl;
    }
    
    
}





int main()
{
    const int NUM_STUDENTS = 50;

    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
   
    //declare the user variable
    double user;
    
    //ask user for their height
    cout << "What is your height? " << endl;
    cin >> user;
    
    
    //call this function in order to tell the users where they need to be in the line
    findPosition(NUM_STUDENTS, heights, user);
    
    return 0;
    
}



