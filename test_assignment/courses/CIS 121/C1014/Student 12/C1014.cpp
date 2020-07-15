//C1014.cpp
//this program tells where an added student will be placed in line
//between two indices

#include <iostream>
using namespace std; 

/*here we create a function that completes the binary
and returns to main where the person should be placed 
based on height*/
int placeMe(float x[], int size, float height)
{
    //indicate the low and high indices and divide them to find the middle index
    int low = 0;
    int high = size - 1;
    int mid;    
    
    while (low <= high)
    {
        //mid is inside the for loop to keep running with the function
        mid = (low+high)/2;
        
        if (height == x[mid])
            return mid;
            
        else if (height > x[mid])
            low = mid + 1; //changes the position of low to the mid point
            
        else if (height < x[mid])
            high = mid - 1; //changes the position of high to the mid point
        else
            return 0;
    }
    
    return mid;
}
int main()
{
    //ask the user for height
    cout << "How tall are you in inches? ";
    
    //create a variable that holds the new height
    float ur_height;
    cin >> ur_height;
    
    //array size
    const int NUM_STUDENTS = 50;
    //array name
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    float placed;
    placed = placeMe(heights, NUM_STUDENTS, ur_height);
    
    //output where the person is to be 
    if (placed == 49)
        cout << "You will stand behind the last person in line.";
    else if (placed == 0)
        cout << "You will stand before the first person in line.";
    else
        cout << "You will stand before the person with the index " << placed;
    return 0;
}
