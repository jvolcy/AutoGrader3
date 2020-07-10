//19 Apr. 2017
//C1014

#include <iostream>
using namespace std;

//create a function that goes through the line deciphering where the late spelmanite should go
void gradlinefunc(int numbers, float heights [], double studentsheight)
{
    
     //initially tried putting the shortest/tallest if statements before the while loop but it did not work
      //if (studentsheight < heights[low_index])
   //{ cout << "The spelmanite should be in the front of the line, be on time next time!";}
   
        //if the student is the tallest, but the spelmanite in the back of the line
       //else if (studentsheight > heights[hi_index])
       //{ cout << "The spelmnite should be in the back of the line, be on time next time!";}
        
        //else go through the while loop to figure out where the spelmanite should go
      // else
        //cout << "The spelmanite should get in between " << low_index+1 << " and " << hi_index+1<< ", be on time next time!";
        
        
   //create variables and set them equal to the indeces
   int low_index,hi_index, mid_index;
   double mid_value;
   
   low_index = 0;
   hi_index = numbers-1;
   

   //create a while loop
   while (hi_index-low_index != 1)
   {
       //set mid index equal to the array size minus one
       mid_index = (hi_index+low_index)/2;
       //set the mid value equal to the array index
       mid_value = heights[mid_index];
       //if the studentsheight is greater than the mid value, set the low index equal to the mid value
       if (studentsheight > mid_value)
       {
           low_index = mid_index;
           hi_index = hi_index;
       }
       
       //if the studentsheight is less than the mid value, set the hi index equal to the mid index and keep the low index at zero
       if (studentsheight < mid_value) 
       {
           low_index = 0;
           hi_index = mid_index;
        }
        
        
       //if the spelmanite's height is equal to the mid value, make the low index equal to the mid index and the high index equal to the mid index plus one
       if (studentsheight == mid_value)
       {
           low_index = mid_index;
           hi_index = mid_index+1;
        } 
    }
        //if the spelmanite is the shortest,put the spelmanite in the front
       if (studentsheight < heights[low_index])
   { cout << "The spelmanite should be in the front of the line, be on time next time!";}
   
        //if the student is the tallest, but the spelmanite in the back of the line
       else if (studentsheight > heights[hi_index])
       { cout << "The spelmnite should be in the back of the line, be on time next time!";}
        
        //else go through the while loop to figure out where the spelmanite should go
       else
        cout << "The spelmanite should get in between " << low_index+1 << " and " << hi_index+1<< ", be on time next time!";
}

//create a main function
int main()
{
    //set the student's height a double 
    double Student_Height;
    
    //set the array size equal to 50
    const int NUM_STUDENTS = 50;
    
    //the array
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5,
                                    57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 
                                    60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 
                                    65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 
                                    69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    
    //ask user for their height
    cout << "How tall are you?" << endl;
    
    //assign user's input to a variable
    cin >> Student_Height;
    
    //pass the necessary things to the gradline function 
    gradlinefunc(NUM_STUDENTS, heights, Student_Height);
    
    return 0;
}