// C1014 - Graduation Lineup
//A program that prompts student 51 for her height then uses a binary search to find an appropriate place for her in the line. 

#include <iostream>
using namespace std;

//graduation line up function
void gradlinefunc(int stunumbers, float heights [], double stuheight)
{
   //create variables
   int low,hi, mid;
   double mid_value;
   
   // set low index to 0 because you will always start at 0
   low = 0;
   // stunumbers is the size of the array-1 
   hi = stunumbers-1;
   //this creates a range from 0 - 49 . for the indices

   //create a while loop
   while (hi-low != 1)
   {
       mid = (hi+low)/2;
       //set the mid value equal to the array index
       mid_value = heights[mid];
       //if the studentsheight is less than the mid value, set the hi index equal to the mid index and keep the low index at zero
       if (stuheight < mid_value) 
       {
           low = 0;
           hi = mid;
        }
        
        //if the students height is greater than the mid value, set the low index equal to the mid value
       if (stuheight > mid_value)
       {
           low = mid;
           hi = hi;
       }
       
       //if the students height is equal to the mid value, set the low index equal to mid and high index equal to mid + 1
       // puts the value to the right of its twin value
       
       if (stuheight == mid_value)
       {
           low = mid;
           hi = mid+1;
        } 
    }
    
    // if student height is less than the first element, it should be the new first element
	if (stuheight < heights[low])
   { cout << "The spelmanite should be in the front of the line";}
   // if student height is greater than the last element, it should be the new last element
   else if (stuheight > heights[hi])
   { cout << "The spelmnite should be in the back of the line";}
   // if it falls somewhere in between the array, it should be put in between its low and high
   // +1 to transfer for indices to actual placement in the array
   else
   {cout << "The spelmanite should get in between " << low+1 << " and " << hi+1;}

    
}

int main()
{
    double Student_Height;
    
    const int NUM_STUDENTS = 50;
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5,
                                    57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 
                                    60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 
                                    65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 
                                    69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    
    //ask user for their height
    cout << "What is your height?" << endl;
    
    //assign user's input to a variable
    cin >> Student_Height;
    
    //pass the necessary things to the gradline function 
    gradlinefunc(NUM_STUDENTS, heights, Student_Height);
    
    return 0;
}