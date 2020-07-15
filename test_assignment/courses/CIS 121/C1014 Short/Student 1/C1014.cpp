#include <iostream> //include iostream
using namespace std; // use namespace standard 

int binarySearch(float heights[], int NUM_STUDENTS, float height51) //define the binary search function
{
    
    for (int i = 0; i < (NUM_STUDENTS - 1); i++) // iterate through the array's indeces
    {
        if (height51 >= heights[i] && height51 < heights[i +1]) // if the 51st student's height is between two heights
            {return i;} //return the index
    }
 
   
}

int main() //define the main function
{
    const int NUM_STUDENTS = 50; //create a constant for the array's size
    
    //a list of 50 students' heights
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    
    //height51 is the 51st student's height
    float height51;
    //Prompt the user for the height
    cout << "Enter the 51st student's height: ";
    //Receive the user's input
    cin >> height51;
    
    if (height51 < heights[0]) //if the input is smaller than the smallest height
    {
        cout << "Place the student at this index: " << 0 << endl; //place the student at index 0
    }
    
    else if (height51 > heights[NUM_STUDENTS - 1]) //if the input is greater than the greatest height
    {
        cout << "Place the student at this index: " << NUM_STUDENTS << endl; //place the student at index 50
    }
    
    else //if neither edge case is met
    {
        int index = binarySearch(heights, NUM_STUDENTS, height51); //call the binary search function
        cout << "Place the student between these indeces: " << index << " and " << index+1 << endl; //print the results  
    }
    
    return 0; //return a value
}

