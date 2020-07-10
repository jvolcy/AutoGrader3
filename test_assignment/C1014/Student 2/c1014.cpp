// Jerry Volcy
//C1014
//  main.cpp
//  CISY1S2
//
//  Created by Brionna Brown on 4/19/17.
//  Copyright © 2017 Brionna Brown. All rights reserved.
//

#include <iostream>
using namespace std;

void binarySearch(float heights[], int NUM_STUDENTS, double spelmaniteheight)
{
    //low index
    int low = 0;
    // high index
    int high = NUM_STUDENTS - 1;
    //the index of the middle value
    double middleValue;
    //the middle of the part of the array that we're looking at
    int middle;
    
    //while the low and high indices aren't next to each other
    while (high-low != 1)
    {
        //the middle of the array
        middle = (high+low) / 2;
        // the index of the middle of the array
        middleValue = heights[middle];
        // looking at the lesser part of the array
        if ( spelmaniteheight < middleValue )
        {
            low = 0;
            high = middle;
        }
        // looking at the higher part of the array
        if ( spelmaniteheight > middleValue )
        {
            low = middle;
            high = high;
            
        }
        // the height is equal to the middle index
        if ( spelmaniteheight == middleValue )
        {
            low = middle;
            high = middle+1;
        }
    }
    
    // the late student is the shortest
    if ( spelmaniteheight < heights[low] )
    {
        cout << "The Spelmanite should go before the first person " << endl;
    }
    //the late student is the tallest student
    else if ( spelmaniteheight > heights[high] )
    {
        cout << "The Spelmanite should go behind the last person " << endl;
    }
    else{
        // positioning of the last student
        cout << "The Spelmanite should go between person " << low << " and " << high << endl;
    }
    
    

}

int main()
{
    
    const int NUM_STUDENTS = 50;
    //array with heights
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    
    double spelmaniteheight;
    // Enter the height of the late student
    cout<< "Enter the height of the late Spelmanite" << endl;
    //variable of the students height
    cin>> spelmaniteheight;
    
    binarySearch(heights, NUM_STUDENTS, spelmaniteheight);
    
    return 0;
}
