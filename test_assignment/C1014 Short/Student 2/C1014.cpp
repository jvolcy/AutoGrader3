//C1014: Graduation Lineup
//This program accepts a height input by the user and calculates what is their position in line.

//skeleton C++ program template
#include <iostream>
using namespace std;

//define display function
void display(float line[], int pos1, int pos2, float student)
{
//if the student is shorter than the one in position one (which, if so, would be the first person in line)
    if(student<line[pos1])
    //display an output instructing the student to stand in the front of the line
        cout << "Stand in front of the line.";
//otherwise if the student is taller than the one in position two (which, if so, would be the last person in line)
    else if(student>line[pos2])
    //display an output instructing the student to stand in the back of the line
        cout << "Stand in the back of the line.";
//otherwise if the student is the same height as the one in position 1
    else if(student==line[pos1])
    //display an output instructing the student to stand in line behind the one in position 1
        cout << "Stand behind the person at spot " << pos1 + 1 << ".";
//otherwise if the student is the same height as the one in position 2
    else if(student==line[pos2])
    //display an output instructing the student to stand in line behind the one in position 2
        cout << "Stand behind the person at spot " << pos2 + 1 << ".";
//otherwise (if the student is taller than the one in position 1 and shorter than the one in position 2)
    else
    //display an output instructing the student to stand in line between the other two's positions
        cout << "Stand between the person at spot " << pos1 + 1 << " and the person at spot " << pos2 + 1 << ".";
}

//define search function
void search(float array[], int size, float height)
{
//initialize the variables needed for the binary search (lo, mid, hi)
    int lo = 0;
    int hi = size-1;
    int mid = (hi + lo) / 2;
//if the user's height is not greater than the last value in the array or less than the first value in the array, the program will enter the while loop
    if(!(height>array[hi] || height<array[lo]))
    {
    //while hi minus lo is not equal to 1
        while(hi-lo!=1)
        {
        //if the height is greater than or equal to the value of the mid element
            if(height>=array[mid])
            //set lo equal to mid
                lo = mid;
        //otherwise
            else
            //set hi equal to mid
                hi = mid;
        //re-initialize mid equal to hi plus lo divided by 2
            mid = (hi + lo) / 2;
        }
    }
//call the display function
    display(array, lo, hi, height);
}

//define the main function
int main()
{
//use skeleton code to create the array
    const int NUM_STUDENTS = 50;
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
//get the user's height
    float student_height;
    cout << "Enter your height: ";
    cin >> student_height;
//call the search function
    search(heights, NUM_STUDENTS, student_height);
//standard return
    return 0;
}