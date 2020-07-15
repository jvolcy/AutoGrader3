
#include <iostream>
using namespace std;
/*Write a program that prompts student 51 for her height then 
uses a binary search to find an appropriate place for her in the line. 
Verify that your code works for a student shorter than the shortest
student currently in line or taller than the tallest student currently in line.
*/

int main()
{
    const int NUM_STUDENTS = 50;
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};

    //1) Get the students height and assign it to a variable
    cout<<"Please enter your height:";
    float height1;
    cin>>height1; 
    
    //2) Define and initialize the variables for the indexes
    int lo=0;               //Index for low
    int hi=NUM_STUDENTS-1;  //Index for high
    int mid= (lo+hi)/2;     //Index for middle 

    //3) Create a loop for doing the binary search
    while (hi-lo!=1)
    {
        if (heights[mid]<=height1)
        {   lo=mid;
            hi=hi;
        }
        else if (heights[mid]>=height1)
        {   hi=mid;
            lo=lo;
        }
        
         mid= (lo+hi)/2; 
    }
    
    //4) Determine the positions
    if (hi==mid)
    {cout<<"The student should be "<<lo+1<<"th in line"<<endl;}
    else if (lo==mid)
    {
        if (height1<=heights[0])
        {cout<<"You are first";}
        else
        {cout<<"The student should be "<<hi+1<<"th in line"<<endl;}
    } 
return 0;
}
