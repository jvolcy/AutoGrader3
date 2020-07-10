#include <iostream>
using namespace std;

/*
 Write a program that prompts student 51 for her height then uses a binary search to find an appropriate place for her in the line.
 */


double binary_search(double a[], int length, double value) //parameters: array, length, searched value
{
    int position = -1;
    bool found = false;
    
    //Three indeces this time first, middle, and last
    int first = 0;
    int last = length - 1;
    int middle;
    
    //while-if-elseif-else
    while(found == false and first <= last)
    {
        middle = (first + last) / 2;
        if(a[middle] == value)
        {
            found = true;
            position = middle;
            
        }
        else if(a[middle] > value)
        {
            last = middle - 1;
            position = last;
        }
        else
        {
            first = middle + 1;
            position = first;
        }
        
    }
    
    
    return position;
}



int main()
{
    const int NUM_STUDENTS = 50;
    
    double heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    
    double h;
    int top = 0, bottom = NUM_STUDENTS - 1, position = 0;
    
    //cout << top << bottom << mid;
    
    //ask student to input her height
    cout << "enter your height rounded to the nearest 1/4 inch ";
    cin >> h;
    
    
    //compare to shortest and tallest student
    if (h < heights[top])
        cout << "the student should be at the front of the line";
    else if (h > heights[bottom])
        cout << "the student should be at the end of the line";
    
    else
    {
        position = binary_search(heights, NUM_STUDENTS, h) ;
        cout << "the student should stand behind " << position + 1 ;
    }
    
    
    return 0;
};
