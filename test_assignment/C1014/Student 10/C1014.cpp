#include <iostream>
using namespace std;


int main()
{
    //defien the index variable and input variable
    int loIndex;
    int hiIndex;
    float lastStud;
    
    const int NUM_STUDENTS = 50;

    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    
    loIndex=0;
    hiIndex=NUM_STUDENTS;
    cout<<"What is the last students height?";
    cin>> lastStud;
    //create the midpoint of the list of heights by adding the smallest and highest index then dividing by 2
    int midpoint;
    midpoint=loIndex+hiIndex/2;
    
    
    //create a variable of the difference between lo and hi index to use for the loop
    int diff; 
    diff=hiIndex-loIndex;
    //create a while loop to do the binary method to divide thru the loop
    //while loop until the difference = 1
    while(diff!=1)
    {
        if (heights[midpoint]<=lastStud)
        {
            loIndex=midpoint;
            
            
        }    
        
        
        else if (heights[midpoint]>=lastStud)
        {
            hiIndex=midpoint;
        }
        
        //redefine midpoint to keep dividing
        midpoint=(loIndex+hiIndex)/2;
        diff=hiIndex-loIndex;
        
    
    
    }
    
    //if statements to determine output of the position number for each person
    if (hiIndex==midpoint)
    {
        cout<<"The person should be number "<<loIndex+1<<" in line.";
    }
    else if (loIndex==midpoint)
    {
        
        //determine if the input is less than the height at index 0 
        if (lastStud<=heights[0])
        {
            cout<<"This person should be first.";
        }
        else
        {
            cout<<"The person should be number "<<hiIndex+1<<" in line.";
        }
    }    
}



