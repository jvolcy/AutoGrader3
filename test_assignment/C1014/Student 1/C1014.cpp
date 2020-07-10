// Example program
#include <iostream>
#include <string>
using namespace std;
//C1014

int main()
{
    const int NUM_STUDENTS = 50;

    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    double x;
    cout<<"enter your height: ";
    //assign user in put to x
    cin>> x;
    //gets index and value of highest and lowest and middle value
    int highpos = NUM_STUDENTS-1;
    double high = heights[highpos];
    int lowpos = NUM_STUDENTS-NUM_STUDENTS;
    double low = heights [lowpos];
    int midpos = highpos/2;
    double midval = heights[midpos];
    //cout<<high<<endl;
    //cout<<highpos<<endl;
    //cout<<low<<endl;
    //cout<<lowpos<<endl;
    //cout<<midpos<<endl;
    //cout<<midval<<endl;
    //checks to see if it is first last or in middle
    if(x<low)
        {cout<<"You are first";}
    else if(x>high)
        {cout<<"You are last";}
    else if(x==midval)
        {cout<<"you go in position"<<midpos;}
    //if not takes it through loop to get position until low and mid dont equal because 
    //then the number cant go anywhere else
    else
        {while(low!=midval)
            {if(x<midval)
                {high = midval;
                highpos = midpos;
 	            low = low;
 	            lowpos = lowpos;
                midpos = midpos/2;
                midval = heights[midpos];
            //cout<<high<<endl;
            //cout<<highpos<<endl;
            //cout<<low<<endl;
            //cout<<lowpos<<endl;
            //cout<<midpos<<endl;
            //cout<<midval<<endl;
                }
            else
 	            {high = high;
 	            highpos = highpos;
 	            low = midval;
 	            lowpos = midpos;
 	            midpos = (lowpos+highpos)/2;
                midval = heights[midpos];
            //cout<<high<<endl;
            //cout<<highpos<<endl;
            //cout<<low<<endl;
            //cout<<lowpos<<endl;
            //cout<<midpos<<endl;
            //cout<<midval<<endl;
 	            }
 	
            }
        //after while loop will print position
        cout<<"you go after ofposition "<<lowpos;
        }
    
    
    return 0;
    

}