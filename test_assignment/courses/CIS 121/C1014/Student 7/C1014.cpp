/* 
Program C1014

ask for user input , and place them in a line of currently existing students  

4/21/2017


*/ 
#include <iostream>
using namespace std;






/*Define the function
is void because doesnt need to return anything

pass  on the array, the array size, and the user input
*/
void binarySearch(float heights[], int NUM_STUDENTS,float user_input)

{
    
    int lo_index, mid_index, hi_index;
    
    //mid=heights[mid_index];
    hi_index=NUM_STUDENTS -1;
    lo_index=0;
    
    
            


    //mid_index = (hi_index + lo_index / 2);

    /* Binary search loop
    while the hi index and lo index isnt right next to each other
    perform the loop */
    while(hi_index-lo_index != 1)
    {
        //formula for the binary search, get the mid point value(index)
        mid_index = (hi_index + lo_index )/ 2;
        //this is the actualy height value in the array
        //mid=heights[mid_index];
        

        //if the user input is less than the mid value
        if(heights[mid_index] < user_input)
        {
            /*set lo to the same value
            set hi to the mid index value */
            lo_index=mid_index;
            hi_index=hi_index; 
            //mid_index = (hi_index + lo_index / 2);

        }
        //if the user input is greater than the mid value
        else if (heights[mid_index] > user_input)
        {
            /* lo index is equal to the mid index
            hi index is the same*/
            hi_index=mid_index;
            lo_index=lo_index;
            //mid_index = (hi_index + lo_index / 2);
        }
        //if its equal
        else if (heights[mid_index] ==user_input)
        
        {
            //lo is equal to mid and hi is equal to mid plus 1
            lo_index=mid_index;
            hi_index=mid_index+1;
            //mid_index = (hi_index + lo_index / 2);
            
        }    
        
    }    
        
        
        //if the user input is less than the lowest height in the line put  them in front   
    if(user_input <heights[lo_index])
    {
        cout <<" You should be placed before the first person in line!";
        
    }
    // if the user input is less than the highest height in the line put them in the back
     else if(user_input > heights[hi_index])
    {
        
        
        cout << "You should be placed after the last person in line";
    }
    // anywhere in between
    else
    {
    
    
    cout << "The student should be in between students number " << lo_index + 1 << " and  "<< hi_index +1 ;
    }
}



//Always need main function
int main()
{

    //given to us
    const int NUM_STUDENTS = 50;

    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    

    //define the variable
    float user_input;
    

    //print out a statement and then set the user input equal to the variable
    cout << "Please enter your height in inches: " ;
    cin >> user_input;

    //call the function
    binarySearch(heights,NUM_STUDENTS,user_input);
    

    
    return 0; 
}