#include <iostream>
#include <cmath>
using namespace std;

//Zari McFadden - Graduation Lineup - Apr. 17, 2017

void binary_search (float X[], int height, int high, int low)
{
    int mid;
    mid = (high + low)/2;               //set mid to (high + low)/ 2
    
    while (high - low != 1)             //while high - low does not equal 1, enter this loop
    
    {
        if (X[mid] < height)            //if value at mid is less than the height
        {
            low = mid;                  //set low to the mid
            mid = (high + low)/2;       //recalculate mid with the new low
        }
        
        else if (X[mid] > height)       //if value at mid is greater than the height
        {
            high = mid;                 //set high to the mid
            mid = (high + low)/2;       //recalculate mid with the new high
            
        }
        else                            //if mid is equal to the height
        {
            low = mid;                  //set low to the mid and keep high the same
            
        }

    }
    
    if (height < X[low])                //if height is less than the lowest value
        high = low;                     //set high equal to low
    
    if (height > X[high])               //if height is greater than the highest value
        low = high;                     //set low equal to high

    
    if (high == low)                                          //if high equals low
        cout << "Place student at index: " << low << '\n';    //only print the low
    
    else
    {
        //else print both high and low
        cout << "Place student between indexes: " << low << " and " << high << '\n';
    }

    
}

void printArray(float X[], int size)    //create print array function
{
    cout << "{";                        //print opening bracket
    
    for (int i = 0; i < size; i ++)     //loop through the array
        cout << X[i] << ", ";           //print each number with a space and comma between them
    
    cout << "}" << '\n';                //print ending bracket

}

int main()
{
    const int NUM_STUDENTS = 50;
    
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};

    
    float student_height;                  //declare student_height a float
    
    printArray(heights, NUM_STUDENTS);     //call print array function to print the heights array
    
    cout << "------------------------------------------" << '\n';
    
    cout << "Enter your height: " << " ";  //user enters their height
    cin >> student_height;                 //user entered height is assigned to student_height
    
    while (student_height <= 0)            //input validation to make sure value is greater than 0
    {
        cout << "Number is 0 or less. Enter a new height: " << " ";
        cin >> student_height;
    }
    
    binary_search(heights, student_height, NUM_STUDENTS, 0); //call binary search function
    
    
    return 0;                              //return 0 to close main function

}
